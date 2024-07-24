import time
from typing import Dict, Any
import logging

from moviepy.editor import VideoFileClip

from backend.src.utils.app_init import init_gemini_llm
from backend.src.utils.helper import check_file_type
from backend.src.utils.constants import VIDEO

import google.generativeai as genai

# video_file_name = "backend/data/BigBuckBunny_320x180.mp4"

def generate_notes(file_path: str):
    model = init_gemini_llm()

    if check_file_type(file_path) == VIDEO:
        video_file = upload_video_file(file_path)

        prompt = "Describe this video"
        response = model.generate_content([video_file, prompt],
                                    request_options={"timeout": 600})
        # response = model.generate_content('Tell me a story about a magic backpack')
        # llm = ChatGoogleGenerativeAI(model = 'gemini-1.5-pro', google_api_key=GOOGLE_API_KEY, temperature = 0)
        # response = llm.invoke("Write me a ballad about LangChain")
        # return response.content

        genai.delete_file(video_file.name)
        logging.info(f'Deleted file {video_file.uri}')

        return response.text


def upload_video_file(file_path):

    video_metadata = get_video_metadata(file_path)
    logging.info(f"metadata: {video_metadata}")
        
    video_file_name = file_path
    logging.info(f"Uploading file...")
    video_file = genai.upload_file(path=video_file_name)
    logging.info(f"Completed upload: {video_file}")

    if video_metadata['duration'] >= 7200:
        logging.info(f"Duration of the video is {video_metadata['duration']}")
        raise ValueError("Video file is too long. Make sure it does not exceed 2 hours.")

    while video_file.state.name == "PROCESSING":
        print('.', end='')
        time.sleep(10)
        video_file = genai.get_file(video_file.name)


    if video_file.state.name == "FAILED":
        raise ValueError(video_file.state.name)
    
    return video_file


def get_video_metadata(file_path: str) -> Dict[Any, Any]:
    try:
        clip = VideoFileClip(file_path)
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
    