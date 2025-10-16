#提供商service
from typing import Optional, List

from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy.util import await_only

from app.schemas.provider import ProviderCreate, ProviderResponse, ProviderUpdate
from app.data.models import Provider
from sqlalchemy import  select,update,delete


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


    async def get_by_id(self,provider_id:int) -> Optional[ProviderResponse] :
        """根据id 查询提供商信息"""
        #1.使用session.get() 方法获取通过组件高级查询
        provider=await self.db.get(Provider,provider_id)

        #2. 检查是否找到记录
        if provider:
            #3. 如果找到。将ORM 模型装好魏Pydantic 想要模型返回
            return ProviderResponse.model_validate(provider)
        #4. 如果没找到返回 none
        return None


    async def get_by_name(self,name:str) -> Optional[ProviderResponse] :
        """根据模型名称查询提供商"""
        # 1. 执行一个SELECT 查询
        result=await self.db.execute(
            select(Provider).where(Provider.name==name)
        )

        #2. 从结果中提前单个标量（Scalar）对象
        provider=result.scalar_one_or_none()
        if provider:
            return ProviderResponse.model_validate(provider)
        return  None

    async  def get_all(self) -> List[ProviderResponse]:
        """获取所有提供商"""

        result=await self.db.execute(select(Provider).order_by(Provider.id.desc()))
        #2. 获取结果中所有标量对象
        providers=result.scalars().all()

        #3. 使用列表推导式将所有ORM对象装好成Pydantic 响应模型
        provider_responses=[ProviderResponse.model_validate(p) for p in providers]

        # 返回Pydantic 模型租车的列表
        return provider_responses

    async  def update(self,provider_id:int,provider_data:ProviderUpdate) -> Optional[ProviderResponse] :
        """更新 提供商"""
        # 1. 检查要更新的 提供商是否合法
        existing_provider=await self.get_by_id(provider_id)
        if not existing_provider:
            return None
        #2 .将Pydantic 输入模型装好魏用于更新的字典
        update_data=provider_data.model_dump(exclude_unset=True)

        #3 如果有数据需要更新，执行数据库操作
        if update_data:
            await self.db.execute(
                update(Provider)
                .where(Provider.id==provider_id)
                .values(**update_data)
            )

            await self.db.commit()

        #4. 更新获取并返回更新后的完整数据
        return  await self.get_by_id(provider_id)

    async def delete(self,provider_id:int) -> bool :
        """删除提供商"""
        #1.检查要删除的提供商是否存在
        existing_provider=await self.get_by_id(provider_id)
        if not existing_provider:
            return False

        #2.执行删除操作
        await  self.db.execute(
            delete(Provider)
            .where(Provider.id==provider_id)
        )

        #3.提交事务 ，使删除生效
        await self.db.commit()

        #4.返回True表示删除成功
        return True

