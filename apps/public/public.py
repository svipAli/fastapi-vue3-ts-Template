from fastapi import APIRouter, Request
from model_types.public_types import *
from utils.public_utils import *

public_app = APIRouter()


@public_app.post("/register", description="这是注册接口")
async def register(request: Request, register_info: UserRegister):
    return await util_register(register_info)
