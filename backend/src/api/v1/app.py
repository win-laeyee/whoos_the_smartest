import logging

from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException

from backend.src.utils.app_init import configure_genai
from backend.src.utils.notes_generation import generate_notes
from backend.src.api.v1.models.requests import FilePathRequest, UserLoginRequest, UserSignupRequest, DeleteMediaRequest, DeleteCollectionsRequest
from backend.src.api.v1.models.responses import NotesGenerateResponse, UserSignupResponse, UserLoginResponse, WelcomeResponse, DeleteMediaResponse, DeleteCollectionsResponse
from backend.src.firebase.firebase_init import initialize_firebase
from backend.src.firebase.database import add_to_notes, delete_firestore_collection

import google.generativeai as genai

from firebase_admin import auth, firestore


app = FastAPI()
security = HTTPBearer()
firebase = initialize_firebase()
db = firestore.client()

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
    file: FilePathRequest,
    user=Depends(verify_token)
):
    
    notes = generate_notes(file.file_path)
    user_id = user['uid']
    add_to_notes(db, user_id, notes)

    return NotesGenerateResponse(summarised_notes=notes)


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
    
    delete_firestore_collection(db, coll_name, batch_size, user_id)

    return DeleteCollectionsResponse(message=f"Deleted '{coll_name}' collection")

