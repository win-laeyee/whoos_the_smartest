import os

from backend.src.utils.constants import IMAGE, PDF_DOCUMENT, PPT_SLIDE, VIDEO, WORD_DOCUMENT


def check_file_type(file_path: str) -> str:
    """
    Determines the type of the file based on its extension.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The file type as a string, such as 'PDF', 'WORD', 'IMAGE', 'VIDEO', or 'PRESENTATION_SLIDES'.

    Raises:
        ValueError: If the file type is unknown.
    """
    _, ext = os.path.splitext(file_path)

    ext = ext.lower()

    if ext == '.pdf':
        return PDF_DOCUMENT
    elif ext == '.docx' or ext == ".doc":
        return WORD_DOCUMENT
    elif ext == '.pptx' or ext == '.ppt':
        return PPT_SLIDE
    elif ext == '.mp4' or ext == '.mov' or ext == '.avi':
        return VIDEO
    elif ext == '.jpg' or ext == '.jpeg' or ext == '.png':
        return IMAGE
    else:
        raise ValueError("Unknown File Type")