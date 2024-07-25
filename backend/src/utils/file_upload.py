import time, logging

from typing import Any, Dict
import google.generativeai as genai
from google.generativeai.types import File
from moviepy.editor import VideoFileClip
from backend.src.utils.constants import IMAGE, VIDEO


def get_video_metadata(video_path: str) -> Dict[Any, Any]:
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
        print(f"An error occurred: {e}")
        return {}


def upload_video_file(video_path: str) -> File:

    video_metadata = get_video_metadata(video_path)
    logging.info(f"metadata: {video_metadata}")

    if video_metadata['duration'] >= 7200:
        logging.info(f"Duration of the video is {video_metadata['duration']}")
        raise ValueError("Video file is too long. Make sure it does not exceed 2 hours.")

    video_file_name = video_path
    logging.info(f"Uploading file...")
    video_file = genai.upload_file(path=video_file_name)
    logging.info(f"Completed upload: {video_file}")
    print(f"Completed upload: {video_file}")

    while video_file.state.name == "PROCESSING":
        print('.', end='')
        time.sleep(10)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError(video_file.state.name)

    return video_file


def upload_image_file(image_path):
    image_file = genai.upload_file(path=image_path)
    logging.info(f"Completed upload: {image_file}")
    print(f"Completed upload: {image_file}")

    return image_file


def upload_file(file_path: str, file_type: str):
    if file_type == VIDEO:
        return upload_video_file(file_path)
    elif file_type == IMAGE:
        return upload_image_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
