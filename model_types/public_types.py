from typing import List, Dict, Union
from pydantic import BaseModel


class ResultTemplate(BaseModel):
    """
    :param code:状态码，0为成功，-1为失败
    :param message:返回文本消息
    :param data:返回的数据
    """
    code: int
    message: str
    data: Union[Dict, List, None]


class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str
