import os
from backend.src.utils.constants import PDF_DOCUMENT, WORD_DOCUMENT, IMAGE, VIDEO, PPT_SLIDE

def check_file_type(file_path: str) -> str:
    _, ext = os.path.splitext(file_path)
    
    ext = ext.lower()
    
    if ext == '.pdf':
        return PDF_DOCUMENT
    elif ext == '.docx' or ext == ".doc":
        return WORD_DOCUMENT
    elif ext == '.pptx' or ext == '.ppt':
        return PPT_SLIDE
    elif ext == '.mp4':
        return VIDEO
    elif ext == '.jpg' or ext == '.jpeg' or ext == '.png':
        return IMAGE
    else:
        raise ValueError("Unknown File Type")
