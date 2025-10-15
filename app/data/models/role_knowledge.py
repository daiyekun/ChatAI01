#角色与知识库中间表模型（多对多）
from sqlalchemy import  Table,Column,Integer,ForeignKey

from app.data.models.base import Base

role_knowledge=Table(
    "role_knowledge",
     Base.metadata,
    Column("role_id",Integer,ForeignKey("role.id"),primary_key=True),
     Column("knowledge_base_id",Integer,ForeignKey("knowledge_base.id"),primary_key=True),

)