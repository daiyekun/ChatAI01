

from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.data.db import  getdb
from app.schemas.message import MessageResponse,ChatRequest
from app.schemas.session import SessionResponse,SessionCreate,SessionUpdate,SessionListResponse
from app.service.message import MessageService
from app.service.session import SessionService
from typing import List

router=APIRouter(prefix="/sessions",tags=["会话管理"])

@router.post("/",response_model=SessionResponse,status_code=201)
async def create_session(session_data:SessionCreate,db: AsyncSession = Depends(getdb)):
    """创建会话"""
    service=SessionService(db)

    try:
        session=await service.create(session_data)
        return  session
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"创建会话失败 {str(e)}"
        )

@router.delete("/{session_id}",status_code=204)
async  def delete_session(session_id: int,db: AsyncSession = Depends(getdb)):
    service=SessionService(db)
    try:
        success=await  service.delete(session_id)
        if success:
            raise  HTTPException(
                status_code=404,
                detail=f"会话ID {session_id} 不存在"
            )
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"删除会话失败 {str(e)}"
        )

@router.get("/{session_id}/messages",response_model=List[MessageResponse])
async  def get_messages(session_id: int
                        ,limit:int=Query(50,ge=1,le=100,description="限制返回消息数量")
                        , db: AsyncSession = Depends(getdb)
                        ):

    """根据会话ID获取消息列表"""

    service=MessageService(db)

    try:
        messages=await  service.getConversation_history(session_id,limit)
        return messages
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取消息列表失败 {str(e)}"
        )

@router.delete("messages/{message_id}/",status_code=204)
async def delete_message(message_id: int,db: AsyncSession = Depends(getdb)):
    service=MessageService(db)

    try:
        success=await service.delete(message_id)
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"消息{message_id} 不存在"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"删除消息失败{str(e)}"
        )

@router.post("/chat",response_model=MessageResponse)
async  def chat(chat_request:ChatRequest,db: AsyncSession = Depends(getdb)):
    service=MessageService(db)

    try:
        response=await service.chat(chat_request)
        return  response
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"处理聊天请求失败 {str(e)}"
        )
