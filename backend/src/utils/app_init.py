import json
import logging
import google.generativeai as genai

from langchain_google_genai import ChatGoogleGenerativeAI


def configure_genai():
    with open('backend/secrets/google_gemini_credentials.json') as f:
        secrets = json.load(f)

    GOOGLE_API_KEY=secrets['GOOGLE_API_KEY']
    genai.configure(api_key=GOOGLE_API_KEY)


def init_gemini_llm():
    configure_genai()
    
    model = genai.GenerativeModel('gemini-1.5-pro')
    return model




def configure_logging(log_level: int = logging.INFO):
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

