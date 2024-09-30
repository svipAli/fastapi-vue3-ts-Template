from fastapi import APIRouter, Depends
from utils.public_utils import *

public_app = APIRouter()


@public_app.post("/register", summary="用户注册")
async def register(register_info: UserRegister):
    return await util_register(register_info)


@public_app.post("/login", summary="用户登录")
async def login(login_info: UserLogin = Depends()):
    return await util_login(login_info)


@public_app.get("/user", summary="获取个人信息")
async def user(username: str = Depends(get_current_user)):
    return await util_user(username)
