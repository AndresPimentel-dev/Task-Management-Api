from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class TaskCreate(BaseModel):
    title: str
    description: str
    status: str

class Token(BaseModel):
    access_token: str
    token_type: str