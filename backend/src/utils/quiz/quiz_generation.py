import logging
import textwrap
from typing import Dict, List, Any, Union

from google.generativeai import GenerativeModel
from google.cloud.firestore_v1.client import Client

from backend.src.api.v1.models.requests import QuizCustomisationRequest
from backend.src.api.v1.models.responses import FreeResponseQuestion, MultiSelectQuestion, MultipleChoiceQuestion, TrueFalseChoices, TrueFalseQuestion, StudentQuizEvaluationResponse
from backend.src.utils.constants import NOTE_COLLECTION, QUIZ_FORMATTER
from backend.src.utils.firestore.notes_operations import retrieve_notes_doc_from_firestore
from backend.src.utils.json_utils import load_json_response


def check_and_format_question_answer_list(quiz_qn_and_ans_list: List[Dict[str, Any]]) -> List[Union[MultipleChoiceQuestion, MultiSelectQuestion, TrueFalseQuestion, FreeResponseQuestion]]:
    """
    Validates and formats a list of question and answer dictionaries.

    Args:
        quiz_qn_and_ans_dict (List[Dict[str, Any]]): The dictionary containing the list of questions and answers.

    Returns:
        List[Union[MultipleChoiceQuestion, MultiSelectQuestion, TrueFalseQuestion, FreeResponseQuestion]]: A list of validated and formatted question objects.

    Raises:
        ValueError: If the input dictionary is missing required keys.
    """

    valid_questions_and_answers = []

    for qn_and_ans in quiz_qn_and_ans_list:
        if 'question' not in qn_and_ans or 'answer' not in qn_and_ans:
            raise ValueError(f"Missing 'question' or 'answer' key in: {qn_and_ans}")

        question = qn_and_ans['question']
        answer = qn_and_ans['answer']

        if 'choices' in qn_and_ans:
            if isinstance(answer, list):
                valid_questions_and_answers.append(MultiSelectQuestion(**qn_and_ans))
            elif isinstance(answer, int):
                valid_questions_and_answers.append(MultipleChoiceQuestion(**qn_and_ans))
            elif answer in [TrueFalseChoices.TRUE.value, TrueFalseChoices.FALSE.value]:
                valid_questions_and_answers.append(TrueFalseQuestion(**qn_and_ans))
            elif isinstance(answer, str) and not qn_and_ans["choices"]:
                valid_questions_and_answers.append(FreeResponseQuestion(question=question, answer=answer))
            else:
                raise ValueError(f"Invalid answer type for question with choices: {qn_and_ans}")
        else:
            if isinstance(answer, str) and isinstance(question, str) and set(qn_and_ans.keys()).issubset({'question', 'answer', 'explanation'}):
                valid_questions_and_answers.append(FreeResponseQuestion(**qn_and_ans))
            else:
                raise ValueError(f"Invalid question and answer type for the question: {qn_and_ans}")

    return valid_questions_and_answers


def get_quiz_customisation_params(quiz_customisation: QuizCustomisationRequest) -> Dict[str, Union[str, int]]:
    """
    Retrieves quiz customization parameters from a request object.

    Args:
        quiz_customisation (QuizCustomisationRequest): The request object containing customization options.

    Returns:
        Dict[str, Union[str, int]]: A dictionary of quiz customization parameters.
    """
    return {
        'number_of_questions': quiz_customisation.number_of_questions or 10,
        'question_types': ', '.join(quiz_customisation.question_types) if quiz_customisation.question_types else "multiple_choice, multi_select, true_false, fill_in_the_blank, short_answer, long_answer",
        'difficulty_level': quiz_customisation.difficulty_level or 'mix',
        'include_explanation': "Yes" if quiz_customisation.include_explanations else "No",
        'emphasis': quiz_customisation.emphasis_custom if quiz_customisation.emphasis == 'other' else quiz_customisation.emphasis or 'balanced',
        'language': quiz_customisation.language or 'English'
    }


def get_quiz_from_content(content: str, 
                          model: GenerativeModel, 
                          number_of_questions: int, 
                          question_types: str, 
                          difficulty_level: str, 
                          include_explanation: str, 
                          emphasis: str, 
                          language: str) -> str:
    """
    Generates quiz questions based on the provided content and customization options.

    Args:
        content (str): The text content to generate quiz questions from.
        model (GenerativeModel): The generative model to use for generating quiz questions.
        number_of_questions (int): The number of questions to generate.
        question_types (str): The types of questions to generate.
        difficulty_level (str): The difficulty level of the questions.
        include_explanation (str): Whether to include explanations for the answers.
        emphasis (str): The emphasis for the quiz questions.
        language (str): The preferred language for the quiz.

    Returns:
        str: The generated quiz in JSON format.
    """

    prompt = f"""
    Please generate {number_of_questions} quiz questions and answers based on the following text. 
    The question types should include: {question_types}.
    The difficulty level of the questions should be: {difficulty_level}.
    Include explanations for the answers: {include_explanation}.
    Emphasize: {emphasis if emphasis else 'balanced'}
    Preferred language for the quiz: {language}

    """

    response = model.generate_content(textwrap.dedent(prompt) + QUIZ_FORMATTER + content, generation_config={'response_mime_type':'application/json'})

    return response.text


def generate_quiz(model: GenerativeModel, db: Client, user_id: str, quiz_customisation: QuizCustomisationRequest) -> List[Dict[str, Any]]:
    """
    Generates a quiz based on the user's notes and customization options.

    Args:
        model (GenerativeModel): The generative model to use for generating quiz questions.
        db (Client): The Firestore client.
        user_id (str): The ID of the user.
        quiz_customisation (QuizCustomisationRequest): Customization options for generating the quiz.

    Returns:
        List[Dict[str, Any]]: The generated quiz in dictionary format.
    """

    content = retrieve_notes_doc_from_firestore(db, user_id)
    logging.info(f"Retrieved documents from {NOTE_COLLECTION}")

    quiz_customisation_params = get_quiz_customisation_params(quiz_customisation)

    quiz_qn_and_ans = get_quiz_from_content(content, model, **quiz_customisation_params)

    logging.info(f"Generated quizzes. Checking for format ...")

    quiz_qn_and_ans_dict = load_json_response(quiz_qn_and_ans)

    return quiz_qn_and_ans_dict[:min(quiz_customisation_params["number_of_questions"], len(quiz_qn_and_ans_dict))]


def format_strengths_weaknesses_for_quiz_regeneration(content: str, strengths_weaknesses: StudentQuizEvaluationResponse) -> str:
    """
    Formats the content and student's strengths and weaknesses for quiz regeneration.

    Args:
        content (str): The text content to generate quiz questions from.
        strengths_weaknesses (StudentQuizEvaluationResponse): The student's strengths and weaknesses.

    Returns:
        str: The formatted string for quiz regeneration.
    """
    formatted_str = content + "\n\n"

    strengths = strengths_weaknesses.strength
    weaknesses = strengths_weaknesses.weakness

    formatted_str += "Student's Strengths:\n"
    formatted_str += f"- {strengths}\n\n"

    formatted_str += "Student's Weaknesses:\n"
    formatted_str += f"- {weaknesses}\n"

    return formatted_str


def get_quiz_from_content_and_student_evaluation(content: str, 
                                                 model: GenerativeModel, 
                                                 number_of_questions: int, 
                                                 question_types: str, 
                                                 difficulty_level: str, 
                                                 include_explanation: str, 
                                                 emphasis: str, 
                                                 language: str, 
                                                 strength_weakness: StudentQuizEvaluationResponse) -> str:
    """
    Generates quiz questions based on the content and student's evaluation.

    Args:
        content (str): The text content to generate quiz questions from.
        model (GenerativeModel): The generative model to use for generating quiz questions.
        number_of_questions (int): The number of questions to generate.
        question_types (str): The types of questions to generate.
        difficulty_level (str): The difficulty level of the questions.
        include_explanation (str): Whether to include explanations for the answers.
        emphasis (str): The emphasis for the quiz questions.
        language (str): The preferred language for the quiz.
        strength_weakness (StudentQuizEvaluationResponse): The student's strengths and weaknesses.

    Returns:
        str: The generated quiz in JSON format.
    """

    prompt = f"""
    Please generate {number_of_questions} quiz questions and answers based on this text and the student's assessment. 
    The question types should include: {question_types}. Choose the most appropriate questions based on the content and assessment of the student's strengths and weaknesses. You should focus more on the weakness.
    The difficulty level of the questions should be: {difficulty_level}.
    Include explanations for the answers: {include_explanation}.
    Emphasize: {emphasis if emphasis else 'balanced'}
    Preferred language for the quiz: {language}

    """

    context = format_strengths_weaknesses_for_quiz_regeneration(content, strength_weakness)

    response = model.generate_content(textwrap.dedent(prompt) + QUIZ_FORMATTER + context, generation_config={'response_mime_type':'application/json'})

    return response.text


def regenerate_quiz_based_on_evaluation(model: GenerativeModel, 
                                        db: Client, 
                                        user_id: str, 
                                        quiz_customisation: QuizCustomisationRequest, 
                                        strength_weakness: StudentQuizEvaluationResponse) -> Dict[str, List[Dict[str, Any]]]:

    """
    Regenerates a quiz based on the student's evaluation and customization options.

    Args:
        model (GenerativeModel): The generative model to use for generating quiz questions.
        db (Client): The Firestore client.
        user_id (str): The ID of the user.
        quiz_customisation (QuizCustomisationRequest): Customization options for generating the quiz.
        strength_weakness (StudentQuizEvaluationResponse): The student's strengths and weaknesses.

    Returns:
        Dict[str, List[Dict[str, Any]]]: The regenerated list of questions and answers in dictionary format.
    """

    content = retrieve_notes_doc_from_firestore(db, user_id)
    logging.info(f"Retrieved documents from {NOTE_COLLECTION}")

    quiz_customisation_params = get_quiz_customisation_params(quiz_customisation)

    quiz_qn_and_ans = get_quiz_from_content_and_student_evaluation(content, model, **quiz_customisation_params, strength_weakness=strength_weakness)
    logging.info(f"Generated quizzes. Checking for format ...")

    quiz_qn_and_ans_dict = load_json_response(quiz_qn_and_ans)

    return quiz_qn_and_ans_dict