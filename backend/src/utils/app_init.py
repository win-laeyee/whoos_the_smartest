import json
import logging

import google.generativeai as genai
from google.generativeai import GenerativeModel
from langchain_google_genai import GoogleGenerativeAIEmbeddings

import firebase_admin
from firebase_admin import credentials
import pyrebase
from pyrebase.pyrebase import Firebase


def configure_genai() -> None:
    """
    Configures the Google Generative AI API with the API key.
    """
    with open('backend/secrets/google_gemini_credentials.json') as f:
        secrets = json.load(f)

    GOOGLE_API_KEY=secrets['GOOGLE_API_KEY']
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
    if not firebase_admin._apps:
        cred = credentials.Certificate("backend/secrets/firebase_service_account_key.json")
        firebase_admin.initialize_app(cred)

    with open('backend/secrets/firebase_sdk.json') as f:
        firebase_config = json.load(f)

    firebase = pyrebase.initialize_app(firebase_config)

    return firebase

