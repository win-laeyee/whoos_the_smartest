from pydantic import BaseModel

class NotesGenerateResponse(BaseModel):
    summarised_notes: str


class UserSignupResponse(BaseModel):
    message: str

class WelcomeResponse(BaseModel):
    message: str

class UserLoginResponse(BaseModel):
    message: str
    idToken: str

class DeleteMediaResponse(BaseModel):
    message: str

class DeleteCollectionsResponse(BaseModel):
    message: str