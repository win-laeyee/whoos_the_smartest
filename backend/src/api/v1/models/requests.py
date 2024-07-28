from pydantic import BaseModel

class FilePathRequest(BaseModel):
    file_path: str


class UserSignupRequest(BaseModel):
    email:str
    password:str


class UserLoginRequest(BaseModel):
    email:str
    password:str

class DeleteMediaRequest(BaseModel):
    file_name: str


class DeleteCollectionsRequest(BaseModel):
    coll_name: str
    batch_size: int