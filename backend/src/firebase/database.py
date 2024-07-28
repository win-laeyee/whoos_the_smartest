import logging
from datetime import datetime, timedelta
from firebase_admin import firestore
from typing import List, Dict, Any, Optional

import google.generativeai as genai
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure

from langchain_experimental.text_splitter import SemanticChunker
from langchain.schema import Document

from backend.src.utils.app_init import configure_genai, init_embedding_model
from backend.src.utils.constants import USER_COLLECTION, NOTE_COLLECTION


def add_to_notes(db: firestore.Client, user_id: str, notes: str) -> None:
    """
    Adds chunked and embedded notes to the Firestore database for a specified user.

    Args:
        db (firestore.Client): The Firestore client.
        user_id (str): The ID of the user.
        notes (str): The notes to be chunked and added.
    """
    notes_split = chunk_text(notes)
    logging.info(f"Chunked notes into {len(notes_split)} chunks.")
    for note_doc in notes_split:
        note = note_doc.page_content
        note_embeddings = embed_text(note)
        notes = {"summarised_notes": note, "embedding": note_embeddings, "timestamp": firestore.SERVER_TIMESTAMP}
        update_time, note_ref = db.collection(USER_COLLECTION).document(user_id).collection(NOTE_COLLECTION).add(notes)
        logging.info(f'Added document with id {note_ref.id} at {update_time}')

# TODO
def get_all_docs_in_notes():
    """
    Placeholder function to retrieve all documents in notes.
    """
    pass

def get_recent_documents(db: firestore.Client, user_id: str, coll_name: str, minutes: Optional[int]=15) -> List[Dict[str, Any]]:
    """
    Retrieves recent documents from a specified collection within a given time frame.

    Args:
        db (firestore.Client): The Firestore client.
        user_id (str): The ID of the user.
        coll_name (str): The name of the collection.
        minutes (Optional[int]): The time frame in minutes. Defaults to 15.

    Returns:
        List[Dict[str, Any]]: A list of recent documents.
    """
    now = datetime.utcnow()
    time_threshold = now - timedelta(minutes=minutes)
    logging.info("Current Time (UTC):", now)
    logging.info("Time Threshold (UTC):", time_threshold)
    
    query = db.collection(USER_COLLECTION).document(user_id).collection(coll_name).where('timestamp', '>=', time_threshold)
    docs = query.stream()
    documents = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data['id'] = doc.id
        documents.append(doc_data)
    
    return documents

def update_notes_with_timestamp(db: firestore.Client, user_id: str) -> None:
    """
    Updates all documents in the user's notes collection with the current server timestamp.

    Args:
        db (firestore.Client): The Firestore client.
        user_id (str): The ID of the user.
    """
    note_ref = db.collection(USER_COLLECTION).document(user_id).collection(NOTE_COLLECTION)
    docs = note_ref.get()
    for doc in docs:
        doc_ref = note_ref.document(doc.id)
        doc_ref.update({"timestamp": firestore.SERVER_TIMESTAMP})
        logging.info(f'Updated document id {doc.id} with timestamp')



def delete_firestore_collection(db: firestore.Client, coll_name: str, batch_size: int, user_id: Optional[str] = None) -> None:
    """
    Recursively deletes documents in a specified collection up to the batch size limit.

    Args:
        db (firestore.Client): The Firestore client.
        coll_name (str): The name of the collection.
        batch_size (int): The maximum number of documents to delete in a batch.
        user_id (Optional[str]): The ID of the user (required for non-user collections).

    Raises:
        ValueError: If user_id is not provided for non-user collections.
    """
    if coll_name == USER_COLLECTION:
        coll_ref = db.collection(coll_name)
    elif user_id and coll_name != USER_COLLECTION: 
        coll_ref = db.collection(USER_COLLECTION).document(user_id).collection(coll_name)
    else:
        raise ValueError(f"Provide user_id to delete collections under 'users' collection.")
    
    if batch_size == 0:
        return

    docs = coll_ref.list_documents(page_size=batch_size)
    deleted = 0

    for doc in docs:
        logging.info(f"Deleting doc {doc.id} => {doc.get().to_dict()}")
        doc.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_firestore_collection(db, coll_name, batch_size, user_id)

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

    logging.info(f"Retrieved {len(retrieved_documents)} from the 'notes' collection")
    
    retrieved_text_lst = []
    for doc in retrieved_documents:
        doc_dict = doc.to_dict()
        retrieved_text_lst.append(doc_dict['summarised_notes'])
    
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
