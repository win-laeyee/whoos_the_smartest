# File types
PDF_DOCUMENT = "PDF"
WORD_DOCUMENT = "WORD"
IMAGE = "IMAGE"
VIDEO = "VIDEO"
# PPT_SLIDE = "PRESENTATION_SLIDES"
IMAGE_MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png"
}
VIDEO_MIME_TYPES = {
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
}

# Collection names
USER_COLLECTION = 'users'
NOTE_COLLECTION = 'notes'
QUIZ_COLLECTION = 'quiz_qn_and_ans'


# Prompts
QUIZ_FORMATTER = """Please return JSON list of questions and answers from this text using the following schema:

    list[MultipleChoice, MultiSelect, TrueFalse, FillInTheBlank, ShortAnswer, LongAnswer]

    MultipleChoice = {"question": str, "choices": list[str], "answer": int, "explanation": str}
    MultiSelect = {"question": str, "choices": list[str], "answer": list[int], "explanation": str}
    TrueFalse = {"question": str, "choices": ["True", "False"], "answer": str, "explanation": str}
    FillInTheBlank = {"question": str, "answer": str, "explanation": str}
    ShortAnswer = {"question": str, "answer": str, "explanation": str}
    LongAnswer = {"question": str, "answer": str, "explanation": str}
   
    All other fields are required.

    Important: Only return a single piece of valid JSON text.

    Here is the text:
    """