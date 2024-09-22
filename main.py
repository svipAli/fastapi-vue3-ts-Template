import os
import time
import uvicorn
from dotenv import load_dotenv  # 引入环境变量文件读取的库
from fastapi import FastAPI, Request  # 引入fastapi
from apps.backend.backend import backend  # 引入后端路由
from apps.public.public import public_app
from fastapi.middleware.gzip import GZipMiddleware
from tortoise.contrib.fastapi import register_tortoise  # 引入tortoise-orm工具注册
from database.settings import TORTOISE_ORM  # 引入tortoise-orm工具的配置
from contextlib import asynccontextmanager  # 引入上下文管理器

load_dotenv(dotenv_path='.env')  # 加载环境变量文件

# 创建FastAPI应用实例
app = FastAPI(
    title=os.getenv('PROJECT_NAME'),
    description=os.getenv('PROJECT_DESCRIPTION'),
    version=os.getenv('PROJECT_VERSION'),
    openapi_url=os.getenv('OPENAPI_URL'),
    docs_url=os.getenv('DOCS_URL'),
    redoc_url=os.getenv('REDOC_URL'),
)

# 注册tortoise-orm映射工具
register_tortoise(app=app, config=TORTOISE_ORM)

app.include_router(backend)  # 管理端默认根目录
app.include_router(public_app, prefix="/public", tags=["这是公共的请求"])  # 管理端默认根目录

app.add_middleware(GZipMiddleware, minimum_size=500)


@asynccontextmanager
async def lifespan(app: FastAPI):  # 里面参数是FastAPI的实例，固定写法
    """程序启动前执行的代码"""

    yield
    """程序关闭执行的代码"""


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
