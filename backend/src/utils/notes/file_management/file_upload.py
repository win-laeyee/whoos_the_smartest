import logging
import time
from typing import Any, Dict

from moviepy.editor import VideoFileClip

import google.generativeai as genai
from google.generativeai.types import File

from backend.src.utils.constants import IMAGE, VIDEO, IMAGE_MIME_TYPES, VIDEO_MIME_TYPES


def get_video_metadata(video_path: str) -> Dict[str, Any]:
    """
    Retrieves metadata from a video file.

    Args:
        video_path (str): The path to the video file.

    Returns:
        Dict[str, Any]: A dictionary containing video metadata such as duration, width, height, and fps.

    Raises:
        Exception: If an error occurs while processing the video file.
    """
    try:
        clip = VideoFileClip(video_path)
        video_metadata = {
            'duration': clip.duration,
            'width': clip.w,
            'height': clip.h,
            'fps': clip.fps
        }
        return video_metadata
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {}


def upload_video_file(video_path: str, ext: str) -> File:
    """
    Uploads a video file to Google Generative AI storage and waits for processing to complete.

    Args:
        video_path (str): The path to the video file.
        ext (str): Extension of the file.

    Returns:
        File: The uploaded video file object.

    Raises:
        ValueError: If the video file is too long or if the upload fails.
    """

    mime_type = VIDEO_MIME_TYPES.get(ext)
    if not mime_type:
        raise ValueError(f"Unsupported video file type: {ext}")


    video_metadata = get_video_metadata(video_path)
    logging.info(f"metadata: {video_metadata}")

    if video_metadata['duration'] >= 7200:
        logging.info(f"Duration of the video is {video_metadata['duration']}")
        raise ValueError("Video file is too long. Make sure it does not exceed 2 hours.")

    video_file_name = video_path
    logging.info(f"Uploading file...")
    try:
        video_file = genai.upload_file(path=video_file_name, mime_type=mime_type)
        logging.info(f"Completed upload: {video_file}")
    except Exception as e:
        logging.error(f"Video upload failed: {e}")
        raise
    logging.info(f"Completed upload: {video_file}")

    while video_file.state.name == "PROCESSING":
        print('.', end='')
        time.sleep(10)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError(video_file.state.name)

    return video_file


def upload_image_file(image_path: str, ext: str) -> File:
    """
    Uploads an image file to Google Generative AI storage.

    Args:
        image_path (str): The path to the image file.
        ext (str): Extension of the file.

    Returns:
        File: The uploaded image file object.

    Raises:
        Exception: If the upload fails.
    """
    try:
        mime_type = IMAGE_MIME_TYPES.get(ext)
        if not mime_type:
            raise ValueError(f"Unsupported video file type: {ext}")

        image_file = genai.upload_file(path=image_path, mime_type=mime_type)
        logging.info(f"Completed upload: {image_file}")
    except Exception as e:
        raise Exception(f"Error occurred: {e}")

    return image_file


def upload_file(file_path: str, file_type: str, ext: str) -> File:
    """
    Uploads a file to Google Generative AI storage based on its type.

    Args:
        file_path (str): The path to the file.
        file_type (str): The type of the file, such as 'VIDEO' or 'IMAGE'.
        ext (str): Extension of the file.

    Returns:
        File: The uploaded file object.

    Raises:
        ValueError: If the file type is unsupported.
    """
    if file_type == VIDEO:
        return upload_video_file(file_path, ext)
    elif file_type == IMAGE:
        return upload_image_file(file_path, ext)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")