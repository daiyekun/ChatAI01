from datetime import datetime
from typing import Optional

from pydantic import  BaseModel,Field

class SessionBase(BaseModel):
    """session 基础DTO模板"""
    title:str=Field(...,max_length=100, description="会话标题")
    role_id:int=Field(...,description="管理角色ID")

class SessionCreate(SessionBase):
    """创建session DTO"""
    pass

class SessionUpdate(SessionBase):
    """更新DTO"""
    title:Optional[str]=Field(None,max_length=100,description="会话标题")
    role_id:Optional[int]=Field(None,description="关联角色ID")

class SessionResponse(SessionBase):
    """响应DTO"""
    id:int=Field(...,description="会话ID")
    create_at:datetime=Field(...,description="创建时间")
    message_count:Optional[int]=Field(None,description="消息数量")

    class Config:
        from_attributes = True

class SessionListResponse(BaseModel):
    """Session 列表响应DTO模板"""
    id:int=Field(...,description="会话ID")
    title:str=Field(...,description="会话标题")
    create_at:datetime=Field(...,description="创建时间")
    role_name:str=Field(...,description="角色名称")

    class Config:
        from_attributes=True
