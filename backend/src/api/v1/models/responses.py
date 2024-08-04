from pydantic import BaseModel, Field
from typing import List, Union, Optional
from enum import Enum

class NotesGenerateResponse(BaseModel):
    summarised_notes: str = Field(..., description="The summarised notes generated from the provided content")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "summarised_notes": "These are the summarised notes from the given document."
                }
            ]
        }
    }

class Correctness(int, Enum):
    CORRECT = 1
    INCORRECT = 0


class EvaluateQuizResponse(BaseModel):
    correctness: Correctness = Field(..., description="Indicates whether the answer is correct or incorrect")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "correctness": 1
                }
            ]
        }
    }

class MultipleChoiceQuestion(BaseModel):
    question: str = Field(..., description="The quiz question")
    answer: int = Field(..., description="The index of the correct answer")
    choices: List[str] = Field(..., description="A list of answer choices")
    explanation: Optional[str] = Field("", description="Explanation behind the answer")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "What is the capital of France?",
                    "answer": 1,
                    "choices": ["Berlin", "Paris", "Madrid", "Rome"]
                }
            ]
        }
    }


class MultiSelectQuestion(BaseModel):
    question: str = Field(..., description="The quiz question")
    answer: List[int] = Field(..., description="Indices of the correct answers")
    choices: List[str] = Field(..., description="A list of answer choices")
    explanation: Optional[str] = Field("", description="Explanation behind the answer")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "Select the prime numbers.",
                    "answer": [0, 2],
                    "choices": ["2", "4", "5", "9"]
                }
            ]
        }
    }


class TrueFalseChoices(str, Enum):
    TRUE = "True"
    FALSE = "False"


class TrueFalseQuestion(BaseModel):
    question: str = Field(..., description="The quiz question")
    answer: TrueFalseChoices = Field(..., description="The correct answer")
    choices: List[TrueFalseChoices] = Field(default=[TrueFalseChoices.TRUE, TrueFalseChoices.FALSE], description="The answer choices, true or false")
    explanation: Optional[str] = Field("", description="Explanation behind the answer")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "The Earth is flat.",
                    "answer": "False",
                    "choices": ["True", "False"]
                }
            ]
        }
    }


class FreeResponseQuestion(BaseModel):
    question: str = Field(..., description="The quiz question")
    answer: str = Field(..., description="The correct answer")
    explanation: Optional[str] = Field("", description="Explanation behind the answer")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "Explain the theory of relativity.",
                    "answer": "The theory of relativity is a fundamental principle in physics, developed by Albert Einstein..."
                }
            ]
        }
    }


class QuizGenerateResponse(BaseModel):
    questions_and_answers: List[Union[MultipleChoiceQuestion, MultiSelectQuestion, TrueFalseQuestion, FreeResponseQuestion]] = Field(..., description="List of generated quiz questions and answers")


class StudentQuizEvaluationResponse(BaseModel):
    score: int = Field(..., description="The student's score on the quiz")
    strength: str = Field(..., description="The student's strength based on quiz performance")
    weakness: str = Field(..., description="The student's weakness based on quiz performance")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "score": 85,
                    "strength": "Strong understanding of concepts",
                    "weakness": "Needs improvement in problem-solving"
                }
            ]
        }
    }


class UserSignupResponse(BaseModel):
    message: str = Field(..., description="Signup response message")


class WelcomeResponse(BaseModel):
    message: str = Field(..., description="Welcome message")


class UserLoginResponse(BaseModel):
    message: str = Field(..., description="Login response message")
    idToken: str = Field(..., description="The ID token for the logged-in user")


class DeleteMediaResponse(BaseModel):
    message: str = Field(..., description="Response message for media deletion")


class DeleteCollectionsResponse(BaseModel):
    message: str = Field(..., description="Response message for collection deletion")

class QueryBotResponse(BaseModel):
    answer: str = Field(..., description="Query bot's answer for user query")
