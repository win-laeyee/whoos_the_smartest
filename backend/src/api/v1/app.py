from fastapi import FastAPI
from backend.src.utils.app_init import init_gemini_llm
from backend.src.api.v1.models.requests import SampleRequest
from backend.src.api.v1.models.responses import SampleResponse

app = FastAPI()

@app.get("/")
def healthcheck():
    return {"status": "ok"}


@app.post("/api/test", response_model=SampleResponse)
def test(
    request_body: SampleRequest
):
    model = init_gemini_llm()
    response = model.generate_content('Tell me a story about a magic backpack')

    return SampleResponse(random_string=response.text)



