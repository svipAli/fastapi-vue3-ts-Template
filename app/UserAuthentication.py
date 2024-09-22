import os
import jwt
import time
from hashlib import md5
from datetime import datetime, timedelta, timezone
from typing import Union
from passlib.context import CryptContext
from dotenv import load_dotenv  # 引入环境变量文件读取的库
from database.models.models import User
from model_types.public_types import UserEncryptDataToken, Token

load_dotenv(dotenv_path='../.env')  # 加载环境变量文件
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def password_encrypt(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate_user(user_data: User, password: str) -> bool:
    return pwd_context.verify(password, user_data.password)


async def create_access_token(user_data: User) -> Token:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    timestamp = str(int(time.time() * 1000))
    user_data = UserEncryptDataToken(
        username=user_data.username,
        timestamp=timestamp,
        sign=md5((user_data.username + "@" + timestamp).encode('utf-8')).hexdigest(),
        exp=expire
    ).__dict__
    return Token(
        access_token=jwt.encode(user_data, SECRET_KEY, algorithm=ALGORITHM),
        token_type="Bearer"
    )


async def verify_token(authorization: Union[str, None]) -> Union[str, None]:
    if authorization is None:
        return None
    if not authorization.startswith("Bearer "):
        return None
    try:
        payload = jwt.decode(authorization[len("Bearer "):], SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        print(e)
        return None
    username: str = payload.get("username")
    timestamp: str = payload.get("timestamp")
    sign: str = payload.get("sign")
    if username is None or timestamp is None or sign is None:
        return None
    if sign != md5((username + "@" + timestamp).encode('utf-8')).hexdigest():
        return None
    return username
