#模型提供商

from sqlalchemy import Column, String,Integer
from app.data.models.base import Base


class Provider(Base):
    __tablename__ = "provider"
    id = Column(Integer, primary_key=True)  # 主键
    name = Column(String,nullable=False)  #程序提供商名称 录入OpenAI
    endpoint= Column(String,nullable=False)  #API 调用地址
    model= Column(String,nullable=False)   # 模型名称 录入gpt-4
    api_key=Column(String,nullable=False)   #api key