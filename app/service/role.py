from typing import Optional,List

from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy import  select,delete,update
from app.data.models import Role,Provider
from app.schemas.role import RoleCreate,RoleUpdate,RoleResponse

class RoleService:
    def __init__(self,db:AsyncSession):
        self.db=db

    async  def create(self,role_create:RoleCreate)->RoleResponse:
        """创建角色"""

         #1.验证provider_id是否存在
        provider=await  self.db.get(Provider,role_create.provider_id)
        if not provider:
            raise ValueError(f"提供商ID {role_create.provider_id} 不存在")

        role_data=role_create.model_dump()
        role=Role(**role_data)
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)

        return RoleResponse.model_validate(role)

    async def get_by_id(self,role_id:int)->Optional[RoleResponse] :
        """根据ID获取角色信息"""
        role=await self.db.get(Role,role_id)
        if role:
            return RoleResponse.model_validate(role)
        return None

    async def get_by_name(self,name:str)->Optional[RoleResponse] :
        """根据名称获取角色"""
        result=await self.db.execute(
            select(Role).where(Role.name==name)
        )
        role=result.scalar_one_or_none()
        if role:
            return RoleResponse.model_validate(role)
        return None

    async def get_all(self)->List[RoleResponse]:
        """查询所有角色"""
        result=await self.db.execute(
            select(Role).order_by(Role.id.desc())
        )

        roles=result.scalars().all()
        role_responses=[RoleResponse.model_validate((r) for r in roles)]
        return role_responses

    async  def update(self,role_id:int,role_data:RoleUpdate)->Optional[RoleResponse] :
        """更新"""
        existing_role=await  self.get_by_id(role_id)
        if not existing_role:
            return None
        if role_data.provider_id is not None:
            provider=await self.db.get(Provider,role_data.provider_id)
            if not provider:
                raise ValueError(f"提供商ID {role_data.provider_id} 不存在")

        update_data=role_data.model_dump(exclude_unset=True )

        if update_data:
            await self.db.execute(
                update(Role).where(Role.id==role_id)
                .values(**update_data)
            )
        await self.db.commit()

        # 4. 更新获取并返回更新后的完整数据
        return await self.get_by_id(role_id)


    async def delete(self,role_id:int) -> bool :
        """删除提供商"""
        #1.检查要删除的提角色是否存在
        existing_role=await self.get_by_id(role_id)
        if not existing_role:
            return False

        #2.执行删除操作
        await  self.db.execute(
            delete(Role)
            .where(Role.id==role_id)
        )

        #3.提交事务 ，使删除生效
        await self.db.commit()

        #4.返回True表示删除成功
        return True


