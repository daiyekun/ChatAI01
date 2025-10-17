from pydantic import  BaseModel,Field
from enum import Enum
from datetime import datetime

class MessageRole(str, Enum):
    """消息角色枚举"""
    User = "user"
    Assistant="assistant"
    System="system"

class MessageBase(BaseModel):
    """消息基础DTO"""
    role:MessageRole=Field(...,description="消息角色 user/assistant/system")
    content:str=Field(...,description="消息内容")
    session_id:int=Field(...,description="关联会话ID")


class MessageResponse(BaseModel):
    """message 响应DTO"""
    id:int=Field(...,description="消息ID")
    create_at:datetime=Field(...,description="创建时间")

    class Config:
        from_attributes=True


class ChatRequest(BaseModel):
    """聊天请求DTO模型"""
    message:str=Field(...,description="消息内容")
    session_id:int=Field(...,description="会话ID")