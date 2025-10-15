#创建数据库引擎
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker

from app.config import DATABASE_URL

#异步创建引擎
engine=create_async_engine(DATABASE_URL,echo=True)

#异步创建session工厂
SessionLocal=async_sessionmaker(engine,expire_on_commit=False)

#FasetAPI 依赖注入函数

async def getdb():
    async with SessionLocal() as session:
        yield session
