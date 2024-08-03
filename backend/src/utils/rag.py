from typing import List, Optional
import logging

from firebase_admin import firestore

from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
import google.generativeai as genai
from google.cloud.firestore_v1.vector import Vector

from langchain.schema import Document
from langchain_experimental.text_splitter import SemanticChunker

from backend.src.utils.app_init import configure_genai, init_embedding_model
from backend.src.utils.constants import NOTE_COLLECTION, USER_COLLECTION


def embed_text(text: str) -> Vector:
    """
    Generates embeddings for the given text using Google Generative AI.

    Args:
        text (str): The text to be embedded.

    Returns:
        Vector: The generated embeddings.
    """
    configure_genai()
    embeddings = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_query")
    vector_embeddings = Vector(embeddings['embedding'])
    return vector_embeddings


def similarity_search_in_notes(db: firestore.Client, user_id: str, embeddings: Vector, limit: Optional[int] = 5) -> List[str]:
    """
    Performs a similarity search in the user's notes collection using the provided embeddings.

    Args:
        db (firestore.Client): The Firestore client.
        user_id (str): The ID of the user.
        embeddings (Vector): The query embeddings.
        limit (Optional[int]): The maximum number of similar texts to retrieve. Defaults to 5.

    Returns:
        List[str]: A list of similar texts.
    """
    embedding_ref = db.collection(USER_COLLECTION).document(user_id).collection(NOTE_COLLECTION)
    retrieved_documents_snapshot = embedding_ref.find_nearest(
            vector_field="embedding",
            query_vector=Vector(embeddings),
            distance_measure=DistanceMeasure.EUCLIDEAN,
            limit=limit
        )

    retrieved_documents = retrieved_documents_snapshot.get()

    logging.info(f"Retrieved {len(retrieved_documents)} from the {NOTE_COLLECTION} collection")

    retrieved_text_lst = []
    for doc in retrieved_documents:
        doc_dict = doc.to_dict()
        retrieved_text_lst.append(doc_dict['summarised_notes'])

    return retrieved_text_lst


def get_most_similar_text(db: firestore.Client, user_id: str, query: str, limit: Optional[int] = 5) -> List[str]:
    """
    Finds the most similar text in the user's notes based on a query.

    Args:
        db (firestore.Client): The Firestore client.
        user_id (str): The ID of the user.
        query (str): The query text.
        limit (Optional[int]): The maximum number of similar texts to retrieve. Defaults to 5.

    Returns:
        List[str]: A list of the most similar texts.
    """
    query_embeddings = embed_text(query)
    retrieved_text_lst = similarity_search_in_notes(db, user_id, query_embeddings, limit)
    return retrieved_text_lst


def chunk_text(notes: str) -> List[Document]:
    """
    Splits notes into smaller chunks using semantic text chunking.

    Args:
        notes (str): The notes to be chunked.

    Returns:
        List[Document]: A list of documents of chunked notes.
    """
    embedding_model = init_embedding_model()

    text_splitter = SemanticChunker(embedding_model, breakpoint_threshold_type="percentile")
    notes_split = text_splitter.create_documents([notes])

    return notes_split