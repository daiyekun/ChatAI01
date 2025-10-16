#文档


from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from sqlalchemy.orm import relationship

from app.data.models.base import Base
from datetime import datetime


class Document(Base):
    __tablename__='document'

    id=Column(Integer,primary_key=True)
    title=Column(String(200),nullable=False)                #文档标题
    source=Column(String(255),nullable=True)               #文档来源活路径
    create_at = Column(DateTime, default=datetime.now())    #创建时间


    #关联知识库ID
    knowledge_base_id=Column(Integer,ForeignKey('knowledge_base.id'),nullable=False)
    #定义关系 文档--》知识库 （多对一）
    knowledge_base=relationship("KnowledgeBase",back_populates="documents")