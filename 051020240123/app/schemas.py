from pydantic import BaseModel
from typing import Optional

class CreateUser(BaseModel):
    username: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    age: Optional[int] = None

class UpdateUser(BaseModel):
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    age: Optional[int] = None

class CreateTask(BaseModel):
    title: str
    content: str
    priority: int

class UpdateTask(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    priority: Optional[int] = None