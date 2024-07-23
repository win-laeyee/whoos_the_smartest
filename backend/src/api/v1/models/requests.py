from pydantic import BaseModel

class SampleRequest(BaseModel):
    random_string: str