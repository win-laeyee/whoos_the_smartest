from fastapi import FastAPI

from backend.src.utils.app_init import configure_genai
from backend.src.utils.generation import generate_notes
from backend.src.api.v1.models.requests import SampleRequest
from backend.src.api.v1.models.responses import SampleResponse

import google.generativeai as genai

app = FastAPI()

@app.get("/")
def healthcheck():
    return {"status": "ok"}


@app.post("/api/get-notes-from-uploaded-file", response_model=SampleResponse)
def get_notes_from_uploaded_file(
    request_body: SampleRequest
):
    response = generate_notes(request_body.random_string)

    return SampleResponse(random_string=response)

@app.post("/api/delete-video")
def delete_video(
    request_body: SampleRequest
):
    configure_genai()
    genai.delete_file(request_body.random_string)

    return SampleResponse(random_string="Video file deleted.")

