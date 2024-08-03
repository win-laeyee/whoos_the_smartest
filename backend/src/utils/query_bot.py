from typing import Optional
from firebase_admin import firestore
from google.generativeai import GenerativeModel

from backend.src.utils.rag import get_most_similar_text
from backend.src.utils.rag import embed_text


def query_firestore(db: firestore.Client, user_id: str, model: GenerativeModel, user_query: str, limit: Optional[int] = 5):
    similar_text_list = get_most_similar_text(db, user_id, user_query, limit)
    print(similar_text_list)
    similar_text = "\n\n ".join(similar_text_list) if len(similar_text_list) > 0 else ""
    answer = answer_user_question(model, user_query, similar_text)

    return answer

def answer_user_question(model: GenerativeModel, user_query: str, similar_text: str):
    prompt = f"""
    You are an expert assistant tasked with generating a comprehensive, well-structured and accurate answer to the user's query based on the provided text.
    
    User's query:
    {user_query}

    Relevant text:
    {similar_text}
    """

    response = model.generate_content(prompt)
    return response.text

