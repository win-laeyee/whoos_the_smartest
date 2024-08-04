from typing import Union
import textwrap

from google.generativeai import GenerativeModel

from backend.src.api.v1.models.responses import FreeResponseQuestion, MultiSelectQuestion, MultipleChoiceQuestion, TrueFalseQuestion
from backend.src.utils.json_utils import load_json_response


def check_free_response_answer(model: GenerativeModel, 
                               question_and_answer: Union[MultipleChoiceQuestion, MultiSelectQuestion, TrueFalseQuestion, FreeResponseQuestion], 
                               student_answer: Union[int, list[int], str]) -> str:
    
    """
    Checks the correctness of a free response answer using a generative model.

    Args:
        model (GenerativeModel): The generative model to use for checking the answer.
        question_and_answer (Union[MultipleChoiceQuestion, MultiSelectQuestion, TrueFalseQuestion, FreeResponseQuestion]): The question and correct answer.
        student_answer (Union[int, list[int], str]): The student's answer to the question.

    Returns:
        str: The response from the model in JSON format.
    """


    prompt = """You are a university professor specializing in exam grading.

    Your task is to evaluate whether the student's answer is correct and sufficiently addresses the question. Please compare the student's answer with the correct answer based on the provided question.

    Return the result in JSON format using the following schema:
    {
        "correctness": int
    }
    Where:
    - 1 indicates the student's answer is correct.
    - 0 indicates the student's answer is incorrect.

    You are provided with the following details:
    """

    context = f"""
    - **Question:** {question_and_answer.question}
    - **Student's Answer:** {student_answer}
    - **Correct Answer:** {question_and_answer.answer}
    """
    response = model.generate_content(textwrap.dedent(prompt) + context, generation_config={'response_mime_type':'application/json'})

    return response.text


def check_student_answer(model: GenerativeModel,
                         question_and_answer: Union[MultipleChoiceQuestion, MultiSelectQuestion, TrueFalseQuestion, FreeResponseQuestion],
                         student_answer: Union[int, list[int], str]) -> int:

    """
    Checks the correctness of a student's answer based on the question type.

    Args:
        model (GenerativeModel): The generative model to use for checking free response answers.
        question_and_answer (Union[MultipleChoiceQuestion, MultiSelectQuestion, TrueFalseQuestion, FreeResponseQuestion]): The question and correct answer.
        student_answer (Union[int, List[int], str]): The student's answer.

    Returns:
        int: 1 if the student's answer is correct, 0 otherwise.
    
    Raises:
        ValueError: If the question type is unsupported.
    """
    if isinstance(question_and_answer, MultipleChoiceQuestion) or isinstance(question_and_answer, TrueFalseQuestion):
        return 1 if student_answer == question_and_answer.answer else 0
    elif isinstance(question_and_answer, MultiSelectQuestion):
        return 1 if sorted(student_answer) == sorted(question_and_answer.answer) else 0
    elif isinstance(question_and_answer, FreeResponseQuestion):
        correctness = check_free_response_answer(model, question_and_answer, student_answer)
        correctness_dict = load_json_response(correctness)
        return correctness_dict["correctness"]
    else:
        raise ValueError("Unsupported question type")