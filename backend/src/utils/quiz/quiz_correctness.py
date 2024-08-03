from typing import Union
import textwrap

from google.generativeai import GenerativeModel

from backend.src.api.v1.models.responses import FreeResponseQuestion, MultiSelectQuestion, MultipleChoiceQuestion, TrueFalseQuestion
from backend.src.utils.json_utils import load_json_response


def check_free_response_answer(model: GenerativeModel, question_and_answer, student_answer):
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