import logging
from typing import Dict, List, Any, Union

from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore_v1.client import Client
from firebase_admin import firestore

from backend.src.utils.constants import QUIZ_COLLECTION, USER_COLLECTION


def add_to_quizzes(db: Client, user_id: str, quiz_qn_and_ans_dict: Dict[str, List[Dict[str, Any]]]) -> None:
    """
    Adds quiz questions and answers to the Firestore database.

    Args:
        db (Client): The Firestore client.
        user_id (str): The ID of the user.
        quiz_qn_and_ans_dict (Dict[str, List[Dict[str, Any]]]): A dictionary containing quiz questions and answers under the key "question_answer_list".

    Returns:
        None
    """
    quizzes = quiz_qn_and_ans_dict["question_answer_list"]
    logging.info(f"Uploading to firestore ...")
    for qna in quizzes:
        qna["timestamp"] = firestore.SERVER_TIMESTAMP
        update_time, quiz_ref = db.collection(USER_COLLECTION).document(user_id).collection(QUIZ_COLLECTION).add(qna)
        logging.info(f'Added document with id {quiz_ref.id} at {update_time}')


def add_student_answer_to_quizzes(db: Client, user_id: str, question: str, student_answer: Union[int, List[int], str], correctness: int) -> None:
    """
    Updates a quiz document with the student's answer and correctness.

    Args:
        db (Client): The Firestore client.
        user_id (str): The ID of the user.
        question (str): The question text to identify the document.
        student_answer (Union[int, List[int], str]): The student's answer to the question.
        correctness (int): Whether the student's answer is correct or not. 1=Correct, 0=Incorrect

    Returns:
        None
    """
    quiz_collection_ref = db.collection(USER_COLLECTION).document(user_id).collection(QUIZ_COLLECTION)
    query = quiz_collection_ref.where(filter=FieldFilter('question', '==', question))
    docs = query.stream()
    for doc in docs:
        doc_ref = quiz_collection_ref.document(doc.id)
        doc_ref.update({"student_answer": student_answer})
        doc_ref.update({"correctness": correctness})
        doc_ref.update({"timestamp": firestore.SERVER_TIMESTAMP})
        logging.info(f'Updated document id {doc.id} with student answer and correctness.')


def get_quiz_results(quiz_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Formats quiz documents into a list of results with relevant fields.

    Args:
        quiz_docs (List[Dict[str, Any]]): A list of quiz document dictionaries.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the question, choices, answer, student answer, correctness, and timestamp.
    """
    quiz_results = [
        {
            "question": doc["question"],
            "choices": doc.get("choices", None),
            "answer": doc["answer"],
            "student_answer": doc.get("student_answer", None),
            "correctness": doc.get("correctness", None),
            "timestamp": doc.get("timestamp", None)
        }
        for doc in quiz_docs
        if doc.get("student_answer") is not None
    ]

    return quiz_results