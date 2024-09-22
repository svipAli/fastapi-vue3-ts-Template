from database.models.models import *
from model_types.public_types import *


async def util_register(register_info: UserRegister) -> ResultTemplate:
    try:
        await User(**register_info.__dict__).save()
        return ResultTemplate(
            code=0,
            message="注册成功",
            data={
                "username": register_info.username
            }
        )
    except Exception as e:
        return ResultTemplate(
            code=-1,
            message=str(e),
            data=None
        )
