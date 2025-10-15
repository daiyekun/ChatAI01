#会话与知识库中间表关系 （多对多）
from sqlalchemy import Table,Integer,ForeignKey,Column
from app.data.models.base import Base

session_knowledge=Table(
    'session_knowledge',
    Base.metadata,
    Column('session_id',Integer,ForeignKey('sessions.id'),primary_key=True  ),
    Column('knowledge_base_id',Integer,ForeignKey('knowledge_base.id'),primary_key=True)
)