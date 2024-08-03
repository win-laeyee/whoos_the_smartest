from typing import Any, Dict, List, Optional
import logging
from datetime import datetime, timedelta

from firebase_admin import firestore
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore_v1.collection import CollectionReference

from backend.src.utils.constants import USER_COLLECTION


def collate_document_data(query: CollectionReference) -> List[Dict[str, Any]]:
    """
    Collects and formats document data from a Firestore collection reference.

    Args:
        query (CollectionReference): The Firestore collection reference object.

    Returns:
        List[Dict[str, Any]]: A list of documents with their data.
    """
    docs = query.stream()
    documents = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data['id'] = doc.id
        documents.append(doc_data)

    return documents


def get_all_docs(db: Client, user_id: str, coll_name: str) -> List[Dict[str, Any]]:
    """
    Retrieves all documents from a specified collection.

    Args:
        db (Client): The Firestore client.
        user_id (str): The ID of the user.
        coll_name (str): The name of the collection.

    Returns:
        List[Dict[str, Any]]: A list of all documents in the collection.
    """
    query = db.collection(USER_COLLECTION).document(user_id).collection(coll_name)
    documents = collate_document_data(query)

    return documents


def get_recent_documents(db: Client, user_id: str, coll_name: str, minutes: Optional[int]=15) -> List[Dict[str, Any]]:
    """
    Retrieves recent documents from a specified collection within a given time frame.

    Args:
        db (Client): The Firestore client.
        user_id (str): The ID of the user.
        coll_name (str): The name of the collection.
        minutes (Optional[int]): The time frame in minutes. Defaults to 15.

    Returns:
        List[Dict[str, Any]]: A list of recent documents.
    """
    now = datetime.utcnow()
    time_threshold = now - timedelta(minutes=minutes)
    logging.info(f"Current Time (UTC): {now}")
    logging.info(f"Time Threshold Time (UTC): {time_threshold}")

    query = db.collection(USER_COLLECTION).document(user_id).collection(coll_name).where(filter=FieldFilter('timestamp', '>=', time_threshold))
    documents = collate_document_data(query)

    return documents


def update_doc_with_timestamp(db: Client, user_id: str, coll_name: str) -> None:
    """
    Updates all documents in the user's notes collection with the current server timestamp.

    Args:
        db (Client): The Firestore client.
        user_id (str): The ID of the user.
        coll_name (str): The name of the collection.
    """
    note_ref = db.collection(USER_COLLECTION).document(user_id).collection(coll_name)
    docs = note_ref.get()
    for doc in docs:
        doc_ref = note_ref.document(doc.id)
        doc_ref.update({"timestamp": firestore.SERVER_TIMESTAMP})
        logging.info(f'Updated document id {doc.id} with timestamp')


def delete_all_docs_in_collection(db: Client, coll_name: str, batch_size: int, user_id: Optional[str] = None) -> None:
    """
    Recursively deletes documents in a specified collection up to the batch size limit.

    Args:
        db (Client): The Firestore client.
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
        return delete_all_docs_in_collection(db, coll_name, batch_size, user_id)