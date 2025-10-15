#角色

from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.data.models.base import Base


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False)         #名称
    description=Column(String,nullable=True)     #描述
    system_prompt=Column(String,nullable=True)   #系统提示词
    temperature=Column(Float,default=0.7)        #模型温度

    #关系模型提供商ID
    provider_id=Column(Integer,ForeignKey('provider.id'),nullable=False)
    #定义了模型之间关系 角色-->提供商 （多对一）
    provider=relationship("Provider")

    #定义模型直接按关系 角色-->会话（一对多）
    sessions=relationship("Session",back_populates="role",cascade="all, delete-orphan")

    #定义关系 角色-->知识库（多对多）
    knowledge_bases=relationship("KnowledgeBase",secondary="role_knowledge",back_populates="roles")

