import json
from typing import Any

from backend.src.utils.exceptions import JSONLoadError


def load_json_response(llm_answer: str) -> Any:
    """
    Loads a JSON response from a string.

    Args:
        llm_answer (str): The string containing the JSON response.

    Returns:
        Any: The decoded JSON object.

    Raises:
        JSONLoadError: If the JSON cannot be decoded or the input is not a string.
    """
    try:
        llm_answer_dict = json.loads(llm_answer)
        return llm_answer_dict
    except json.JSONDecodeError as e:
        raise JSONLoadError(f"Failed to decode JSON: {e}")
    except TypeError as e:
        raise JSONLoadError(f"Input should be a string, but got: {type(llm_answer)}")
    except Exception as e:
        raise JSONLoadError(f"An unexpected error occurred: {e}")