from typing import Optional

from google.generativeai import GenerativeModel
from google.cloud.firestore_v1.client import Client

from backend.src.utils.rag import get_most_similar_text
from backend.src.utils.rag import embed_text


def query_firestore(db: Client, user_id: str, model: GenerativeModel, user_query: str, limit: Optional[int] = 5) -> str:
    """
    Queries Firestore for similar text to a user's query and generates an answer.

    Args:
        db (Client): The Firestore client.
        user_id (str): The ID of the user.
        model (GenerativeModel): The generative model to use for answering the query.
        user_query (str): The user's query.
        limit (Optional[int]): The maximum number of similar texts to retrieve. Defaults to 5.

    Returns:
        str: The generated answer to the user's query.
    """
    similar_text_list = get_most_similar_text(db, user_id, user_query, limit)
    similar_text = "\n\n ".join(similar_text_list) if len(similar_text_list) > 0 else ""
    answer = answer_user_question(model, user_query, similar_text)

    return answer

def answer_user_question(model: GenerativeModel, user_query: str, similar_text: str) -> str:
    """
    Generates an answer to the user's query based on provided similar text.

    Args:
        model (GenerativeModel): The generative model to use for generating the answer.
        user_query (str): The user's query.
        similar_text (str): The text similar to the user's query.

    Returns:
        str: The generated answer.
    """
    
    prompt = f"""
    You are an expert assistant tasked with generating a comprehensive, well-structured and accurate answer to the user's query based on the provided text.
    
    User's query:
    {user_query}

    Relevant text:
    {similar_text}
    """

    response = model.generate_content(prompt)
    return response.text

