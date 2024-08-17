from typing import Any, Dict, Union
import logging
import os

from google.generativeai.types import File
from google.generativeai import GenerativeModel

from backend.src.api.v1.models.requests import NotesCustomisationRequest
from backend.src.utils.constants import IMAGE, PDF_DOCUMENT, VIDEO, WORD_DOCUMENT #,PPT_SLIDE
from backend.src.utils.notes.file_management.file_check import check_file_type
from backend.src.utils.notes.file_management.file_cleanup import cleanup_file
from backend.src.utils.notes.file_management.file_upload import upload_file
from backend.src.utils.notes.text_extraction import extract_text


def generate_notes_from_content(content: Union[str, File], model: GenerativeModel, customisation: Dict[str, str], content_type: str) -> str:
    """
    Generates notes from provided content (media or document) using a generative model.

    Args:
        content (Union[str, File]): A media file or document to generate notes from.
        model (GenerativeModel): The generative model to use for generating notes.
        customisation (Dict[str, str]): The customisation settings.
        content_type (str): The type of content ('media' or 'document').

    Returns:
        str: The generated notes.
    """
    prompt = f"""
    You are a skilled note-taker tasked with summarizing the content of a {content_type} file.
    Please generate well-structured notes with headings and bullet points for easier readability based on the following preferences:
    - Focus: {customisation['focus'] if customisation['focus'] else 'General'}
    - Tone: {customisation['tone'] if customisation['tone'] else 'neutral'}
    - Emphasis: {customisation['emphasis'] if customisation['emphasis'] else 'balanced'}
    - Length: {customisation['length'] if customisation['length'] else 'standard'}
    - Language: {customisation['language']}

    {f'{content_type.capitalize()} file content:' if content_type == 'media' else 'Extracted text:'}
    {content if content_type == 'document' else ''}
    """

    if content_type == 'media':
        response = model.generate_content([content, prompt], request_options={"timeout": 600})
    else:
        response = model.generate_content(prompt)

    return response.text


def get_notes_customisation_params(notes_customisation: NotesCustomisationRequest) -> Dict[str, str]:
    """
    Returns the actual notes customisation settings based on the user's preferences.

    Args:
        notes_customisation (NotesCustomisationRequest): The customisation options.

    Returns:
        Dict[str, str]: The actual customisation settings.
    """
    return {
        'focus': notes_customisation.focus_custom if notes_customisation.focus == 'other' else notes_customisation.focus,
        'tone': notes_customisation.tone_custom if notes_customisation.tone == 'other' else notes_customisation.tone,
        'emphasis': notes_customisation.emphasis_custom if notes_customisation.emphasis == 'other' else notes_customisation.emphasis,
        'length': notes_customisation.length_custom if notes_customisation.length == 'other' else notes_customisation.length,
        'language': notes_customisation.language if notes_customisation.language else 'English'
    }


def generate_notes(model: GenerativeModel, file_path: str, file_name: str, notes_customisation: NotesCustomisationRequest) -> str:
    """
    Generates notes from a file based on its type. Handles media and document files.

    Args:
        model (GenerativeModel): The generative model to use for generating notes.
        file_path (str): The path to the file from which to generate notes.
        file_name (str): Name of the file with extension
        notes_customisation (NotesCustomisationRequest): The customisation options.

    Returns:
        str: The generated notes.

    Raises:
        FileNotFoundError: If the file does not exist at the given path.
        ValueError: If the file type is unsupported.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")

    file_type, ext = check_file_type(file_name)

    actual_customisation = get_notes_customisation_params(notes_customisation)

    if file_type in [VIDEO, IMAGE]:
        file = upload_file(file_path, file_type, ext)
        notes = generate_notes_from_content(file, model, actual_customisation, content_type="media")
        cleanup_file(file)
    elif file_type in [PDF_DOCUMENT, WORD_DOCUMENT]: #, PPT_SLIDE]:
        extracted_text = extract_text(file_path, file_type)
        notes = generate_notes_from_content(extracted_text, model, actual_customisation, content_type="document")

    logging.info(f"Generated notes for file {file_path}.")

    return notes