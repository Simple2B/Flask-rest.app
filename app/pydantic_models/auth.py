#  from typing import Optional
from pydantic import BaseModel, Field
from flask_openapi3 import FileStorage


class Regist_Model(BaseModel):
    username: str = Field("test_user1", description='username')
    email: str = Field("test_user5@email.com", description='email')
    password: str = Field("test_user1@password", description='password')


class Login_Model(BaseModel):
    username: str = Field("test_user1", description='username')
    email: str = Field("test_user5@email.com", description='email')
    password: str = Field("test_user1@password", description='password')


class File_Model(BaseModel):
    file: FileStorage
