from typing import Optional

from pydantic import  BaseModel,Field

class RoleBase(BaseModel):
    """role dto 模板"""
    name:str=Field(...,max_length=100,description="角色名称")
    description:Optional[str]=Field(None,max_length=500,description="角色描述")
    system_prompt:Optional[str]=Field(None,description="系统提示词")
    temperature:float=Field(0.7,ge=0.0,le=2.0,description="模型温度")
    provider_id:int=Field(...,description="管理模型提供商ID")

class RoleCreate(RoleBase):
    """传教role模型"""
    pass

class RoleResponse(RoleBase):
    """role 响应DTO"""
    id:int=Field(...,description="角色ID")

    class Config:
        from_attributes=True



class RoleUpdate(RoleBase):
    """更新role dto"""
    name:Optional[str] =Field(None,max_length=100,description="角色名称")
    description:Optional[str]=Field(None,max_length=500,description="角色描述")
    system_prompt:Optional[str]=Field(None,description="系统提示词")
    temperature:Optional[float]=Field(0.7,ge=0.0,le=2.0,description="模型温度")
    provider_id:Optional[int]=Field(None,description="模型提供商ID")
