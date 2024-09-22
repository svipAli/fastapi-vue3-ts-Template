from typing import List, Dict, Union
from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class ResultTemplate(BaseModel):
    """
    :param code:状态码，0为成功，-1为失败
    :param message:返回文本消息
    :param data:返回的数据
    """
    code: int
    message: str
    data: Union[Dict, List, Token, None]


class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserEncryptDataToken(BaseModel):
    username: str
    timestamp: str
    sign: str
    exp: datetime
