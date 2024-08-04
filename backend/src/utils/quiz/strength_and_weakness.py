import logging
from typing import Any, Dict, List, Union
import textwrap

from google.generativeai import GenerativeModel
from google.cloud.firestore_v1.client import Client

from backend.src.utils.constants import QUIZ_COLLECTION
from backend.src.utils.firestore.document_operations import get_recent_documents
from backend.src.utils.firestore.quizzes_operations import get_quiz_results
from backend.src.utils.json_utils import load_json_response


def format_quiz_results(quiz_qn_and_ans_list: List[Dict[str, Any]]) -> str:
    """
    Formats quiz results for display.

    Args:
        quiz_qn_and_ans_list (List[Dict[str, Any]]): A list of dictionaries containing quiz results.

    Returns:
        str: The formatted quiz results as a string.
    """
    formatted_str = ""
    for item in quiz_qn_and_ans_list:
        formatted_str += f"Question: {item.get('question', 'N/A')}\n"
        if 'choices' in item and item['choices'] is not None:
            formatted_str += "Choices:\n"
            for choice in item['choices']:
                formatted_str += f"  - {choice}\n"
        formatted_str += f"Answer: {item.get('answer', 'N/A')}\n"
        formatted_str += f"Student's Answer: {item.get('student_answer', 'N/A')}\n"
        correctness = "Correct" if item.get('correctness') == 1 else "Incorrect"
        formatted_str += f"Correctness: {correctness}\n"
        formatted_str += "-" * 40 + "\n"

    return formatted_str


def evaluate_strength_and_weakeness(model: GenerativeModel, quiz_results: List[Dict[str, Any]]) -> str:
    """
    Evaluates the student's strengths and weaknesses based on quiz results.

    Args:
        model (GenerativeModel): The generative model to use for evaluation.
        quiz_results (List[Dict[str, Any]]): A list of dictionaries containing quiz results.

    Returns:
        str: The evaluation result in JSON format.
    """

    prompt = """You are a university professor who can assess a student's strength and weakness very well given their exam results.

    Your task is to evaluate the student's performance and identify their strengths and weaknesses. Consider the exam results and any relevant details provided. 

    Address the student directly. 

    Return the result in JSON format using the following schema:
    {
        "strength": str,
        "weakness": str
    }

    You are provided with the following details:
    """

    quiz_results_str = format_quiz_results(quiz_results)

    response = model.generate_content(textwrap.dedent(prompt) + quiz_results_str, generation_config={'response_mime_type':'application/json'})

    return response.text


def calculate_student_score(latest_quiz_results: List[Dict[str, Any]]) -> int:
    """
    Calculates the student's score based on the latest quiz results.

    Args:
        latest_quiz_results (List[Dict[str, Any]]): A list of dictionaries containing the latest quiz results.

    Returns:
        int: The student's score as a percentage.
    """
    total_questions = len(latest_quiz_results)
    correct_answers = sum(1 for result in latest_quiz_results if result['correctness'] == 1)
    quiz_score = round((correct_answers / total_questions) * 100) if total_questions > 0 else 0

    return quiz_score


def assess_student_strength_weakness(model: GenerativeModel, db: Client, user_id: str, num_of_quiz_qn: int) -> Dict[str, Union[str, int]]:
    """
    Assesses the student's strengths and weaknesses based on recent quiz results.

    Args:
        model (GenerativeModel): The generative model to use for evaluation.
        db (Client): The Firestore client.
        user_id (str): The ID of the user.
        num_of_quiz_qn (int): The number of quiz questions to consider.

    Returns:
        Dict[str, Union[str, int]]: The student's strengths and weaknesses along with their score.

    Raises:
        ValueError: If there are no recently answered quizzes or if the user did not answer any questions.
    """
    quiz_docs = get_recent_documents(db, user_id, QUIZ_COLLECTION, minutes=num_of_quiz_qn*2)

    if len(quiz_docs) == 0:
        raise ValueError(f"There is no recently answered quizzes. Answer a quiz before getting your score.")

    quiz_results = get_quiz_results(quiz_docs)

    if len(quiz_results) == 0:
        raise ValueError(f"You did not answer any questions. Answer the quiz before getting your score and evaluation.")

    sorted_quiz_results = sorted(quiz_results, key=lambda x: x['timestamp'], reverse=True)
    latest_quiz_results = sorted_quiz_results[:num_of_quiz_qn] if len(sorted_quiz_results) > num_of_quiz_qn else sorted_quiz_results
    logging.info(f"Retrieved quiz results.")

    quiz_score = calculate_student_score(latest_quiz_results)
    logging.info(f"Calculated quiz score: {quiz_score}.")

    strength_weakness = evaluate_strength_and_weakeness(model, latest_quiz_results)
    logging.info(f"Generated strengths and weaknesses.")

    strength_weakness_dict = load_json_response(strength_weakness)

    result_dict = strength_weakness_dict
    result_dict["score"] = quiz_score

    return result_dict