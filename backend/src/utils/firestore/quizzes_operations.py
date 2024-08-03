import logging

from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import firestore

from backend.src.utils.constants import QUIZ_COLLECTION, USER_COLLECTION


def add_to_quizzes(db, user_id, quiz_qn_and_ans_dict):
    quizzes = quiz_qn_and_ans_dict["question_answer_list"]
    logging.info(f"Uploading to firestore ...")
    for qna in quizzes:
        qna["timestamp"] = firestore.SERVER_TIMESTAMP
        update_time, quiz_ref = db.collection(USER_COLLECTION).document(user_id).collection(QUIZ_COLLECTION).add(qna)
        logging.info(f'Added document with id {quiz_ref.id} at {update_time}')


def add_student_answer_to_quizzes(db, user_id, question, student_answer, correctness):
    quiz_collection_ref = db.collection(USER_COLLECTION).document(user_id).collection(QUIZ_COLLECTION)
    query = quiz_collection_ref.where(filter=FieldFilter('question', '==', question))
    docs = query.stream()
    for doc in docs:
        doc_ref = quiz_collection_ref.document(doc.id)
        doc_ref.update({"student_answer": student_answer})
        doc_ref.update({"correctness": correctness})
        doc_ref.update({"timestamp": firestore.SERVER_TIMESTAMP})
        logging.info(f'Updated document id {doc.id} with student answer and correctness.')

def get_quiz_results(quiz_docs):
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