import logging

from tempfile import NamedTemporaryFile
import os
import json

from fastapi import FastAPI, Depends, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException

from backend.src.utils.app_init import configure_genai, init_gemini_llm
from backend.src.utils.firestore.notes_operations import add_to_notes
from backend.src.utils.firestore.quizzes_operations import add_student_answer_to_quizzes, add_to_quizzes
from backend.src.utils.notes.notes_generation import generate_notes
from backend.src.utils.quiz.quiz_generation import check_and_format_question_answer_list, generate_quiz
from backend.src.utils.quiz.quiz_generation import regenerate_quiz_based_on_evaluation
from backend.src.utils.quiz.quiz_correctness import check_student_answer
from backend.src.utils.quiz.strength_and_weakness import assess_student_strength_weakness
from backend.src.utils.query_bot import query_firestore
from backend.src.api.v1.models.requests import FilePathRequest, UserLoginRequest, UserSignupRequest, DeleteMediaRequest, DeleteCollectionsRequest, CompareAnswerRequest, NotesCustomisationRequest, QuizCustomisationRequest, QueryBotRequest, QuizParameterRequest
from backend.src.api.v1.models.responses import NotesGenerateResponse, UserSignupResponse, UserLoginResponse, WelcomeResponse, DeleteMediaResponse, DeleteCollectionsResponse, QuizGenerateResponse, EvaluateQuizResponse, StudentQuizEvaluationResponse, QueryBotResponse
from backend.src.utils.app_init import initialize_firebase
from backend.src.utils.firestore.document_operations import delete_all_docs_in_collection

import google.generativeai as genai

from firebase_admin import auth, firestore


app = FastAPI()
security = HTTPBearer()
firebase = initialize_firebase()
db = firestore.client()

model = init_gemini_llm()

@app.get("/")
def healthcheck():
    return {"status": "ok"}


@app.post('/api/signup', response_model=UserSignupResponse)
async def create_an_account(user_data: UserSignupRequest):
    email = user_data.email
    password = user_data.password

    try:
        user = firebase.auth().create_user_with_email_and_password(email, password)
        return UserSignupResponse(message=f"User account created successfully for user {user['localId']}")
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    

@app.post('/api/login', response_model=UserLoginResponse)
async def login(user_data: UserLoginRequest):
    email = user_data.email
    password = user_data.password

    try:
        user = firebase.auth().sign_in_with_email_and_password(email, password)
        return UserLoginResponse(message="Login successful", idToken=user["idToken"])
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    

async def verify_token(auth_creds: HTTPAuthorizationCredentials = Depends(security)):
    token = auth_creds.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        logging.info(f"Token verification failed: {e}") 
        raise HTTPException(
            status_code=401,
            detail="Invalid token or token has expired"
        )

@app.get('/api/protected', response_model=WelcomeResponse)
async def protected_route(user=Depends(verify_token)):
    return WelcomeResponse(message=f"Welcome {user['email']}")


@app.post("/api/get-notes-from-uploaded-file", response_model=NotesGenerateResponse)
def get_notes_from_uploaded_file(
    file: UploadFile = File(...),
    notes_customisation: str = Form(...),
    user=Depends(verify_token)
):
    notes_customisation_dict = json.loads(notes_customisation)
    notes_customisation_object = NotesCustomisationRequest(**notes_customisation_dict)

    # file_dict
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file.file.read())
        temp_file_path = temp_file.name

    notes = generate_notes(model, temp_file_path, file.filename, notes_customisation_object)
    os.remove(temp_file_path)
    user_id = user['uid']
    add_to_notes(db, user_id, notes)

    return NotesGenerateResponse(summarised_notes=notes)


@app.post("/api/get-quiz-from-uploaded-notes", response_model=QuizGenerateResponse)
def get_quiz_from_uploaded_notes(
    quiz_customisation: QuizCustomisationRequest,
    user=Depends(verify_token)
):
    user_id = user['uid']
    
    quiz_qn_and_ans_list = generate_quiz(model, db, user_id, quiz_customisation)
    formatted_quiz_qn_and_ans = check_and_format_question_answer_list(quiz_qn_and_ans_list)

    add_to_quizzes(db, user_id, quiz_qn_and_ans_list)

    return QuizGenerateResponse(questions_and_answers=formatted_quiz_qn_and_ans)


@app.post("/api/evaluate-student-answer", response_model=EvaluateQuizResponse)
def evaluate_student_answer(
    question_and_answers: CompareAnswerRequest,
    user=Depends(verify_token)
):
    user_id = user['uid']
    question_and_answer = question_and_answers.question_and_answer
    student_answer = question_and_answers.student_answer
    
    correctness = check_student_answer(model, question_and_answer, student_answer)

    add_student_answer_to_quizzes(db, user_id, question_and_answer.question, student_answer, correctness)

    return EvaluateQuizResponse(correctness=correctness)



@app.post("/api/get-student-strength-weakness", response_model=StudentQuizEvaluationResponse)
def get_student_strength_and_weakness(
    quiz_parameter: QuizParameterRequest,
    user=Depends(verify_token)
):
    user_id = user['uid']
    
    result_dict = assess_student_strength_weakness(model, db, user_id, quiz_parameter.num_of_qns)

    return StudentQuizEvaluationResponse(score=result_dict["score"],strength=result_dict["strength"], weakness=result_dict["weakness"])


@app.post("/api/regenerate-quiz", response_model=QuizGenerateResponse)
def regenerate_quiz(
    quiz_customisation: QuizCustomisationRequest,
    strength_and_weakness: StudentQuizEvaluationResponse,
    user=Depends(verify_token)
):
    user_id = user['uid']
    
    quiz_qn_and_ans_dict = regenerate_quiz_based_on_evaluation(model, db, user_id, quiz_customisation, strength_and_weakness)
    formatted_quiz_qn_and_ans = check_and_format_question_answer_list(quiz_qn_and_ans_dict)
    
    add_to_quizzes(db, user_id, quiz_qn_and_ans_dict)

    return QuizGenerateResponse(questions_and_answers=formatted_quiz_qn_and_ans)


@app.post("/api/query-bot", response_model=QueryBotResponse)
def query_bot(
    user_query: QueryBotRequest,
    user=Depends(verify_token)
):
    user_id = user['uid']
    bot_answer = query_firestore(db, user_id, model, user_query.query, limit=10)

    return QueryBotResponse(answer=bot_answer)


@app.post("/api/delete-media")
def delete_media(
    file: DeleteMediaRequest
):
    configure_genai()
    genai.delete_file(file.file_name)

    return DeleteMediaResponse(message="Video file deleted.")

@app.post("/api/delete-collections", response_model=DeleteCollectionsResponse)
def delete_collections(
    coll_info: DeleteCollectionsRequest,
    user=Depends(verify_token)
):
    user_id = user['uid']
    coll_name = coll_info.coll_name
    batch_size = coll_info.batch_size
    
    delete_all_docs_in_collection(db, coll_name, batch_size, user_id)

    return DeleteCollectionsResponse(message=f"Deleted '{coll_name}' collection")

