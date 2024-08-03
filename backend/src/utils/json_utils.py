import json

from backend.src.utils.exceptions import JSONLoadError


def load_json_response(llm_answer):
    try:
        llm_answer_dict = json.loads(llm_answer)
        return llm_answer_dict
    except json.JSONDecodeError as e:
        raise JSONLoadError(f"Failed to decode JSON: {e}")
    except TypeError as e:
        raise JSONLoadError(f"Input should be a string, but got: {type(llm_answer)}")
    except Exception as e:
        raise JSONLoadError(f"An unexpected error occurred: {e}")