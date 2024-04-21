# pylint: disable=C0115:missing-class-docstring,C0114:missing-module-docstring
from pydantic import BaseModel

class UserRegistration(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Article(BaseModel):
    content:str
    categories:list[str]
