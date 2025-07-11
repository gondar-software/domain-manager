from pydantic import BaseModel

class Auth(BaseModel):
    password: str

class Token(BaseModel):
    token: str