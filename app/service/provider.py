#提供商service

from sqlalchemy.ext.asyncio import  AsyncSession
from app.schemas.provider import ProviderCreate, ProviderResponse
from app.data.models import Provider


class ProviderService:
    def __init__(self,db:AsyncSession):
        self.db=db

    async  def create(self,provider_create:ProviderCreate) -> ProviderResponse:
        """创建provider"""
        # 1.将DTO装好魏字典
        provider_data=provider_create.model_dump()

        #2.将字典捷豹成（**）来创建ORM模型实例
        provider=Provider(**provider_data)

        #3.将歆的创建ORM 对象添加到数据库会话中
        self.db.add(provider)
        await self.db.commit()

        await self.db.refresh(provider)

        #4.刷新实例，以获取数据库中生成值
        return ProviderResponse.model_validate(provider)

