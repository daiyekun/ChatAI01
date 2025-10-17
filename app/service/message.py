from typing import List
from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy import select,delete
from sqlalchemy.orm import selectinload
from app.data.models import  Message,Session,Role
from app.schemas.message import  MessageRole,MessageBase,MessageResponse,ChatRequest

class MessageService:
     def __init__(self,db:AsyncSession):
         self.db=db


     async  def create(self,message:MessageBase)->MessageResponse:
         """创建消息"""
         session=await self.db.get(Session,message.session_id)
         if not session:
             raise ValueError(f"会话ID {message.session_id} 不存在")

         message_data=message.model_dump()
         message=Message(**message_data)

         self.db.add(message)
         await self.db.commit()
         await self.db.refresh(message)
         return MessageResponse.model_validate(message)


     async  def getConversation_history(self,session_id:int,limit:int=50)->List[MessageResponse]:
         """"查询会话历史记录"""
         result=await self.db.execute(
             select(Message)
             .where(Message.session_id == session_id)
             .order_by(Message.id)
             .limit(limit)
         )

         messages= result.scalars().all()
         return [MessageResponse.model_validate(msg) for msg in messages]

     async  def chat(self,chat_req:ChatRequest)->MessageResponse:
         """处理聊天消息"""
         # 1 验证session 是否存在
         session=await self.db.get(Session,chat_req.session_id)
         if not session:
             raise ValueError(f"会话Id {chat_req.session_id} 不存在")

         #获取会话绑定的角色与模板信息
         role=await self.db.scalar(
             select(Role)
             .options(selectinload(Role.provider))
             .where(Role.id==session.role_id)
         )

         if not role:
             raise  ValueError(f"角色 {role.name} 不存在")

         #获取消息历史
         conversation_history=await self.getConversation_history(chat_req.session_id)

         #这里调用AI服务来生成回复
         #目前先返回以后模拟回复
         assistant_content=(f"我是{role.name } 我们聊了{len(conversation_history)} 条消息 收到您的消息'{chat_req.message}' 模拟回复")

         #创建用户信息
         user_message=MessageBase(
             role=MessageRole.User,
             content=chat_req.message,
             session_id=chat_req.session_id,
             )

         await self.create(user_message)

         #创建助手回复
         assistant_message=MessageBase(
             role=MessageRole.Assistant,
             content=assistant_content,
             session_id=chat_req.session_id,
         )

         res=await self.create(assistant_message)

         return res

     async def delete(self,message_id:int)->bool:
         """删除消息"""
         await self.db.execute(
             delete(Message).where(Message.id == message_id)
         )
         await self.db.commit()
         return True


