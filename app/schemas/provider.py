#提供商DTO
from typing import Optional

from pydantic import BaseModel,Field

class ProviderBase(BaseModel):
    """provider 基础DTO模板"""
    name:str=Field(...,max_length=100,description="提供商名称")
    endpoint:str=Field(...,max_length=255,description="API调用地址")
    model:str=Field(...,max_length=100,description="模型名称")
    api_key:str=Field(...,description="api密钥")


class ProviderCreate(ProviderBase):
    """验证provider的DTO模型"""
    pass
class ProviderResponse(ProviderBase):
    """provider 响应dto"""
    id:int=Field(...,description="提供商ID")

    class Config:#配置模型行为
        from_attributes=True

class ProviderUpdate(ProviderBase):
    """更新DTO"""
    name:Optional[str]=Field(None,max_length=100,description="提供商名称")
    endpoint:Optional[str]=Field(None,max_length=255,description="api调用地址")
    model:Optional[str]=Field(None,max_length=100,description="模型名称")
    api_key:Optional[str]=Field(None,description="api密钥")