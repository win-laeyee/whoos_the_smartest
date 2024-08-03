PDF_DOCUMENT = "PDF"
WORD_DOCUMENT = "WORD"
IMAGE = "IMAGE"
VIDEO = "VIDEO"
PPT_SLIDE = "PRESENTATION_SLIDES"


USER_COLLECTION = 'users'
NOTE_COLLECTION = 'notes'
QUIZ_COLLECTION = 'quiz_qn_and_ans'


QUIZ_FORMATTER = """Please return JSON describing the question and answer from this text using the following schema:

    {"question_answer_list": list[MultipleChoice, MultiSelect, TrueFalse, FillInTheBlank, ShortAnswer, LongAnswer]}

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