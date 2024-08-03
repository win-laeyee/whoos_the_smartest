import firebase_admin
from firebase_admin import credentials
import pyrebase
import json

from pyrebase.pyrebase import Firebase

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
