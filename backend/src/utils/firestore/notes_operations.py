from typing import Any, Dict, List
import logging

from firebase_admin import firestore
from google.cloud.firestore_v1.client import Client

# from backend.src.utils.rag import chunk_text
from backend.src.utils.rag import chunk_text_by_sentence_count
from backend.src.utils.constants import NOTE_COLLECTION, USER_COLLECTION
from backend.src.utils.firestore.document_operations import get_all_docs, get_recent_documents
from backend.src.utils.rag import embed_text



def add_to_notes(db: Client, user_id: str, notes: str) -> None:
    """
    Adds chunked and embedded notes to the Firestore database for a specified user.

    Args:
        db (Client): The Firestore client.
        user_id (str): The ID of the user.
        notes (str): The notes to be chunked and added.
    """
    # notes_split = chunk_text(notes)
    notes_split = chunk_text_by_sentence_count(notes, 5)

    logging.info(f"Chunked notes into {len(notes_split)} chunks. Uploading to firestore ...")
    for note_doc in notes_split:
        # note = note_doc.page_content
        note = note_doc
        if not note or not note.strip():
            continue
        note_embeddings = embed_text(note)
        notes = {"summarised_notes": note, "embedding": note_embeddings, "timestamp": firestore.SERVER_TIMESTAMP}
        update_time, note_ref = db.collection(USER_COLLECTION).document(user_id).collection(NOTE_COLLECTION).add(notes)
        logging.info(f'Added document with id {note_ref.id} at {update_time}')


def get_notes_from_docs(documents: List[Dict[str, Any]]) -> str:
    """
    Aggregates 'summarised_notes' from a list of Firestore document dictionaries into a single string.

    Args:
        documents (List[Dict[str, Any]]): A list of document dictionaries, where each dictionary contains a 'summarised_notes' field.

    Returns:
        str: A concatenated string of all 'summarised_notes' from the documents.
    """
    content = ""

    for doc in documents:
        content += doc['summarised_notes']

    return content


def retrieve_notes_doc_from_firestore(db: Client, user_id: str) -> str:
    """
    Retrieves and aggregates notes from recent documents or all documents if recent ones are empty.

    Args:
        db (Client): The Firestore client.
        user_id (str): The ID of the user.

    Returns:
        str: Aggregated notes content.

    Raises:
        ValueError: If no documents are found in the collection.
    """
    recent_documents = get_recent_documents(db, user_id, NOTE_COLLECTION)
    content = get_notes_from_docs(recent_documents)

    if not content:
        logging.info("No content available from recent documents to generate a quiz. Using all documents in the collection to generate the quiz ...")
        all_documents = get_all_docs(db, user_id, NOTE_COLLECTION)
        content = get_notes_from_docs(all_documents)
        if not content:
            logging.error(f"No documents in {NOTE_COLLECTION} collection.")
            raise ValueError("Upload a file to get started. There is no documents available in our database to generate a quiz.")

    return content