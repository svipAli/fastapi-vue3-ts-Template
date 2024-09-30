from model_types.public_types import *
from app.UserAuthentication import *
from fastapi import Request, HTTPException, status


async def get_current_user(request: Request):
    username = request.state.data['username']
    if not username:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户身份校验失败！",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
    else:
        return username


async def util_register(register_info: UserRegister) -> ResultTemplate:
    register_info_data = register_info.__dict__
    register_info_data['password'] = password_encrypt(register_info_data['password'])
    await User(**register_info_data).save()
    return ResultTemplate(
        code=0,
        message="注册成功",
        data={
            "username": register_info.username
        }
    )


async def util_login(login_info) -> ResultTemplate:
    user_data = await User.filter(username=login_info.username).first()
    if not user_data:
        return ResultTemplate(
            code=0,
            message="账号不存在！",
            data=None
        )
    if await authenticate_user(user_data, login_info.password):
        if user_data.status == 0:
            return ResultTemplate(
                code=0,
                message="登录成功！",
                data=await create_access_token(user_data)
            )
        else:
            return ResultTemplate(
                code=0,
                message="账号已被禁用！",
                data=await create_access_token(user_data)
            )
    else:
        return ResultTemplate(
            code=0,
            message="密码错误！",
            data=await create_access_token(user_data)
        )


async def util_user(username: str) -> ResultTemplate:
    user = await User.filter(username=username).first().values()
    return ResultTemplate(
        code=0,
        message="请求成功！",
        data=user
    )
