import logging

import google.generativeai as genai
from google.generativeai.types import File


def cleanup_file(file: File) -> None:
    """
    Deletes a file from the Google Generative AI storage.

    Args:
        file (File): The file object to be deleted.

    Returns:
        None
    """
    genai.delete_file(file.name)
    logging.info(f'Deleted file {file.uri}')