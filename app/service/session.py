from typing import Optional,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete,update,func
from sqlalchemy.orm import  selectinload
from app.data.models import  Session,Role,Provider,Message
from app.schemas.session import SessionCreate,SessionResponse,SessionUpdate,SessionListResponse


class SessionService:
    def __init__(self,db:AsyncSession):
        self.db=db


    async  def create(self,session_create:SessionCreate):
        """创建session"""
        role=await  self.db.get(Role,session_create.id)
        if role is None:
            raise  ValueError(f"角色 ID {session_create.role_id} 不存在")

        session_data=session_create.model_dump()
        session=Session(**session_data)
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)

        return SessionResponse.model_validate(session)


    async  def get_all(self)->List[SessionListResponse]:
        """获取所欲会话"""
        result=await  self.db.execute(
            select(
                Session.id,
                Session.title,
                Session.create_at,
                Role.name.label("role_name"),
            )
            .outerjoin(Message,Session.id==Message.session_id)
             .join(Role,Session.role_id==Role.id)
             .group_by(Session.id,Session.title,Session.create_at,Role.name,Provider.name)
             .order_by(Session.create_at.desc())
        )

        sessions=result.all()
        return [SessionListResponse(
            id=session.id,
            title=session.title,
            create_at=session.create_at,
            role_name=session.role_name,
        )
        for session in sessions
        ]

    async  def delete(self,session_id:int)->bool:
        """删除会话"""
        await self.db.execute(
            delete(Session).where(Session.id == session_id)
        )
        await self.db.commit()
        return True