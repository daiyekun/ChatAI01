#知识库

from sqlalchemy import Column,Integer,String,Text
from sqlalchemy.orm import relationship

from app.data.models.base import Base

class KnowledgeBase(Base):
    __tablename__='knowledge_base'

    id=Column(Integer,primary_key=True)
    name=Column(String(100),nullable=False)   #知识库名称
    description=Column(Text,nullable=True)    #知识库描述


    #定义关系 知识库-->角色（多对多）
    roles=relationship("Role",secondary='role_knowledge',back_populates="knowledge_base")

    #定义关系 知识库-->会话 （多对多）
    sessions=relationship("Session",secondary="session_knowledge",back_populates="knowledge_base")

    #定义关系 知识库-->文档 一对多
    documents=relationship("Document",back_populates="knowledge_base", cascade="all, delete-orphan")