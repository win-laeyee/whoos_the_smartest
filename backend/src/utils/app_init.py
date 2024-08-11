import json
import logging
from dotenv import load_dotenv
import os

import google.generativeai as genai
from google.generativeai import GenerativeModel
from langchain_google_genai import GoogleGenerativeAIEmbeddings

import firebase_admin
from firebase_admin import credentials
import pyrebase
from pyrebase.pyrebase import Firebase

load_dotenv()

def configure_genai() -> None:
    """
    Configures the Google Generative AI API with the API key.
    """
    GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY", "")
    genai.configure(api_key=GOOGLE_API_KEY)
    return GOOGLE_API_KEY


def init_gemini_llm() -> GenerativeModel:
    """
    Initializes and returns a GenerativeModel instance from the Google Generative AI API.
    """
    configure_genai()
    
    model = genai.GenerativeModel('gemini-1.5-pro')
    return model


def init_embedding_model() -> GoogleGenerativeAIEmbeddings:
    """
    Initializes and returns a GoogleGenerativeAIEmbeddings instance.
    """
    GOOGLE_API_KEY = configure_genai()
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=GOOGLE_API_KEY)
    return embedding_model


def configure_logging(log_level: int = logging.INFO) -> None:
    """
    Configures the logging settings for the application.
    """
    logging.getLogger().handlers.clear()

    logging.basicConfig(
        format="%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
        datefmt="[%Y-%m-%d %H:%M:%S]",
        level=log_level,
    )

    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.error").handlers.clear()
    logging.getLogger("uvicorn.access").propagate = True
    logging.getLogger("uvicorn.error").propagate = True


def initialize_firebase() -> Firebase:
    """
    Initializes Firebase with the provided service account and SDK configurations.
    """
    firebase_service_cred = {
        "type": os.getenv("FIREBASE_TYPE", ""),
        "project_id": os.getenv("FIREBASE_PROJECT_ID", ""),
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID", ""),
        "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL", ""),
        "client_id": os.getenv("FIREBASE_CLIENT_ID", ""),
        "auth_uri": os.getenv("FIREBASE_AUTH_URI", ""),
        "token_uri": os.getenv("FIREBASE_TOKEN_URI", ""),
        "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL", ""),
        "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL", ""),
        "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN", "")
    }
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_service_cred)
        firebase_admin.initialize_app(cred)

    firebase_config = {
        "apiKey": os.getenv("FIREBASE_API_KEY", ""),
        "authDomain": os.getenv("AUTH_DOMAIN", ""),
        "projectId": os.getenv("PROJECT_ID", ""),
        "storageBucket": os.getenv("STORAGE_BUCKET", ""),
        "messagingSenderId": os.getenv("MESSAGING_SENDER_ID", ""),
        "appId": os.getenv("APP_ID", ""),
        "databaseURL": os.getenv("DATABASE_URL", "")
        }

    firebase = pyrebase.initialize_app(firebase_config)

    return firebase

