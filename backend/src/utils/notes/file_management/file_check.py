import os

from backend.src.utils.constants import IMAGE, PDF_DOCUMENT, VIDEO, WORD_DOCUMENT #,PPT_SLIDE


def check_file_type(file_name: str) -> str:
    """
    Determines the type of the file based on its extension.

    Args:
        file_name (str): The name of the file.

    Returns:
        str: The file type as a string, such as 'PDF', 'WORD', 'IMAGE', 'VIDEO', or 'PRESENTATION_SLIDES'.

    Raises:
        ValueError: If the file type is unknown.
    """
    _, ext = os.path.splitext(file_name)

    ext = ext.lower()

    if ext == '.pdf':
        return PDF_DOCUMENT, ext
    elif ext == '.docx':
        return WORD_DOCUMENT, ext
    # elif ext == '.pptx':
    #     return PPT_SLIDE, ext
    elif ext == '.mp4' or ext == '.mov':
        return VIDEO, ext
    elif ext == '.jpg' or ext == '.jpeg' or ext == '.png':
        return IMAGE, ext
    else:
        raise ValueError("Unsupported File Type")