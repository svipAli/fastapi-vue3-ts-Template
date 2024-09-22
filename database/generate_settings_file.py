"""
数据库的配置文件
###注意！使用tortoise-orm工具必须要安装aerich数据库迁移工具库 pip install aerich
支持的数据库
PostgreSQL >= 9.4 (使用asyncpg)

SQLite (使用aiosqlite)

MySQL / MariaDB (使用asyncmy )

Microsoft SQL Server / Oracle（使用asyncodbc）

使用asyncpg的时候需要先 pip install asyncpg
使用Mysql的时候需要先 pip install aiomysql


"""
import os
import json
from dotenv import load_dotenv  # 引入环境变量文件读取的库

load_dotenv(dotenv_path='../.env')  # 加载环境变量文件

TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': os.getenv('DATABASE_ENGINE'),
            'credentials': {
                'host': os.getenv('DATABASE_HOST'),
                'port': os.getenv('DATABASE_PORT'),
                'user': os.getenv('DATABASE_USER'),
                'password': os.getenv('DATABASE_PASSWORD'),
                'database': os.getenv('DATABASE_NAME'),
                # 如果使用的是PostgreSQL 请注释掉以下4行
                # 'minsize': 1,
                # 'maxsize': 5,
                # 'charset': 'utf8mb4',
                # "echo": True
            }
        },
    },
    'apps': {
        'models': {
            'models': [
                # 模型映射文件（.py文件）绝对路径 从项目根目录开始，路径中的 "/" 用 "." 代替，最后的 ".py" 省略。可以多个，映射文件需要在database/models/文件夹下创建模型映射文件
                'database.models.models',

                # 这 aerich.models不需要更改 固定写法
                'aerich.models'
            ],
            'default_connection': 'default',
        }
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}

with open("settings.py", 'w', encoding='utf-8') as f:
    f.write(("TORTOISE_ORM=" + json.dumps(TORTOISE_ORM)).replace('false', 'False').replace('true', 'True'))
