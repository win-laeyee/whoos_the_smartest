from pydantic import BaseModel, Field
from typing import Union, Optional, Literal, List

from backend.src.api.v1.models.responses import MultipleChoiceQuestion, MultiSelectQuestion, TrueFalseQuestion, FreeResponseQuestion

class FilePathRequest(BaseModel):
    file_path: str = Field(..., description="Path to the file")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "file_path": "/path/to/file.txt"
                }
            ]
        }
    }


class UserSignupRequest(BaseModel):
    email: str = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class UserLoginRequest(BaseModel):
    email: str = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class DeleteMediaRequest(BaseModel):
    file_name: str = Field(..., description="Name of the file to be deleted")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "file_name": "file/asjdmcuekwada"
                }
            ]
        }
    }


class DeleteCollectionsRequest(BaseModel):
    coll_name: str = Field(..., description="Name of the collection to be deleted")
    batch_size: int = Field(..., description="Size of the batch for deletion")


class NotesCustomisationRequest(BaseModel):
    focus: Optional[Literal['general', 'specific_concepts', 'examples', 'summary', 'other']] = Field(
        None, description="Focus area for the notes"
    )
    focus_custom: Optional[str] = Field(None, description="Custom focus area for the notes")
    tone: Optional[Literal['formal', 'informal', 'conversational', 'other']] = Field(
        None, description="Preferred tone for the notes"
    )
    tone_custom: Optional[str] = Field(None, description="Custom tone for the notes")
    emphasis: Optional[Literal['key_points', 'details', 'definitions', 'other']] = Field(
        None, description="What to emphasize in the notes"
    )
    emphasis_custom: Optional[str] = Field(None, description="Custom emphasis for the notes")
    length: Optional[Literal['concise', 'moderate', 'detailed', 'other']] = Field(
        None, description="Desired length of the notes"
    )
    length_custom: Optional[str] = Field(None, description="Custom length for the notes")
    language: Optional[Literal[
        'Arabic', 'Bengali', 'Bulgarian', 'Chinese simplified and traditional', 'Croatian', 
        'Czech', 'Danish', 'Dutch', 'English', 'Estonian', 'Finnish', 'French', 'German', 
        'Greek', 'Hebrew', 'Hindi', 'Hungarian', 'Indonesian', 'Italian', 'Japanese', 
        'Korean', 'Latvian', 'Lithuanian', 'Norwegian', 'Polish', 'Portuguese', 'Romanian', 
        'Russian', 'Serbian', 'Slovak', 'Slovenian', 'Spanish', 'Swahili', 'Swedish', 'Thai', 
        'Turkish', 'Ukrainian', 'Vietnamese'
    ]] = Field(None, description="Preferred language for the notes")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "focus": "specific_concepts",
                    "focus_custom": "Deep learning concepts",
                    "tone": "formal",
                    "tone_custom": None,
                    "emphasis": "key_points",
                    "emphasis_custom": None,
                    "length": "detailed",
                    "length_custom": None,
                    "language": "English"
                }
            ]
        }
    }


class QuizCustomisationRequest(BaseModel):
    number_of_questions: Optional[int] = Field(10, description="Number of quiz questions to generate.")
    question_types: Optional[List[Literal['multiple_choice', 'multi_select', 'true_false', 'fill_in_the_blank', 'short_answer', 'long_answer']]] = Field(
        None, description="Types of questions to include in the quiz."
    )
    difficulty_level: Optional[Literal['easy', 'medium', 'hard', 'mix']] = Field(None, description="Preferred difficulty level of the questions.")
    include_explanations: Optional[bool] = Field(False, description="Whether to include explanations for the answers.")
    emphasis: Optional[Literal['key_points', 'details', 'definitions', 'other']] = Field(
        None, description="What to emphasize in the quiz questions"
    )
    emphasis_custom: Optional[str] = Field(None, description="Custom emphasis for the quiz questions.")
    language: Optional[Literal[
        'Arabic', 'Bengali', 'Bulgarian', 'Chinese simplified and traditional', 'Croatian', 
        'Czech', 'Danish', 'Dutch', 'English', 'Estonian', 'Finnish', 'French', 'German', 
        'Greek', 'Hebrew', 'Hindi', 'Hungarian', 'Indonesian', 'Italian', 'Japanese', 
        'Korean', 'Latvian', 'Lithuanian', 'Norwegian', 'Polish', 'Portuguese', 'Romanian', 
        'Russian', 'Serbian', 'Slovak', 'Slovenian', 'Spanish', 'Swahili', 'Swedish', 'Thai', 
        'Turkish', 'Ukrainian', 'Vietnamese'
    ]] = Field(None, description="Preferred language for the quiz questions")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "number_of_questions": 10,
                    "question_types": ["multiple_choice", "multi_select", "true_false", "fill_in_the_blank", "short_answer", "long_answer"],
                    "difficulty_level": "medium",
                    "include_explanations": True,
                    "emphasis": "details",
                    "emphasis_custom": None,
                    "language": "English"
                }
            ]
        }
    }
    
class CompareAnswerRequest(BaseModel):
    student_answer: Union[int, List[int], str] = Field(..., description="Student's answer, can be an integer, a list of integers, or a string")
    question_and_answer: Union[
        MultipleChoiceQuestion, 
        MultiSelectQuestion, 
        TrueFalseQuestion, 
        FreeResponseQuestion
    ] = Field(..., description="Question and answer details, can be of different types")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                   "student_answer": [1, 2],
                    "question_and_answer": {
                         "question": "Select the prime numbers.",
                        "answer": [0, 2],
                        "choices": ["2", "4", "5", "9"]
                    }
                },
                {
                    "student_answer": "ABC",
                    "question_and_answer": {
                        "question": "Explain the theory of relativity.",
                        "answer": "The theory of relativity is a fundamental principle in physics, developed by Albert Einstein..." 
                    }
                }
            ]
        }
    }


class QueryBotRequest(BaseModel):
    query: str = Field(..., description="User's question to query against database")


class QuizParameterRequest(BaseModel):
    num_of_qns: int = Field(..., description="Number of questions in the quiz")
