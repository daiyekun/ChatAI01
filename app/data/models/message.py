#消息
from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey
from datetime import datetime

from sqlalchemy.orm import relationship

from app.data.models.base import Base

class Message(Base):
    __tablename__='message'

    id=Column(Integer,primary_key=True)
    role=Column(String(20),nullable=False)                       #消息角色类型， user/assistant
    content=Column(Text,nullable=False)                          #消息内容
    create_at=Column(DateTime,default=datetime.now())            #创建时间



    #关联会话
    session_id=Column(Integer,ForeignKey('sessions.id'),nullable=False)
    #定义关系 消息--》会话一对多
    session=relationship("Session",back_populates="messages")