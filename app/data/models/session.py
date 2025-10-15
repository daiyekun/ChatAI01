#会话
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from datetime import datetime

from sqlalchemy.orm import relationship

from app.data.models.base import Base



class Session(Base):
    __tablename__='sessions'

    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=False)
    create_at=Column(DateTime,default=datetime.now())


    #关联角色ID
    role_id=Column(Integer,ForeignKey('role.id'),nullable=False)
    #定义模型之间关系 会话-->角色（多对于一）
    role=relationship("Role",back_populates="sessions")

    #定义关系 会话--消息 （一对多）
    messages=relationship("Message",back_populates="session",cascade="all, delete-orphan")

    #定义会话-->知识库 关系（多对多）
    knowledge_bases=relationship("KnowledgeBase",secondary="session_knowledge", back_populates="sessions")