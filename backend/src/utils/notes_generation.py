import os

from google.generativeai.types import File

from backend.src.utils.app_init import init_gemini_llm
from backend.src.utils.file_check import check_file_type
from backend.src.utils.constants import VIDEO, WORD_DOCUMENT, PDF_DOCUMENT, IMAGE, PPT_SLIDE

from backend.src.utils.file_cleanup import cleanup_file
from backend.src.utils.file_upload import upload_file
from backend.src.utils.text_extraction import extract_text


def generate_notes(file_path: str):
    model = init_gemini_llm()

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")
    
    file_type = check_file_type(file_path)

    if file_type in [VIDEO, IMAGE]:
        file = upload_file(file_path, file_type)
        notes = get_notes_from_media(file, model)
        cleanup_file(file)
    elif file_type in [PDF_DOCUMENT, WORD_DOCUMENT, PPT_SLIDE]:
        extracted_text = extract_text(file_path, file_type)
        notes = get_notes_from_document(extracted_text, model)
    
    return notes
   

def get_notes_from_media(media_file: File, model) -> str:
    prompt = "Generate a summary of notes from the media file provided."
    response = model.generate_content([media_file, prompt],
                                request_options={"timeout": 600})
    # response = model.generate_content('Tell me a story about a magic backpack')
    # llm = ChatGoogleGenerativeAI(model = 'gemini-1.5-pro', google_api_key=GOOGLE_API_KEY, temperature = 0)
    # response = llm.invoke("Write me a ballad about LangChain")
    # return response.content

    return response.text



def get_notes_from_document(extracted_text: str, model) -> str:
    prompt = f"Here is the extracted text: \n{extracted_text}\n\nPlease generate a summary or content based on this text."

    response = model.generate_content(prompt)
    print(f"get notes from doc: {response}")
    return response.text








