from email.policy import default

from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import  AsyncSession
from app.data.db import  getdb
from app.schemas.role import RoleResponse, RoleCreate, RoleUpdate
from app.service.role import RoleService

from typing import  List

router=APIRouter(prefix= "/roles",tags=["模型提角色管理"])

@router.post("/",response_model=RoleResponse,status_code=201 )
async  def create_role(prover_data:RoleCreate,db:AsyncSession=Depends(getdb)):
    """创建新的模型提角色"""
    service=RoleService(db)

    try:
        role=await service.create(prover_data)
        return  role
    except Exception as e:
        raise  HTTPException(status_code=500,detail=f"模型提角色创建失败{str(e)}")


@router.get("/",response_model=List[RoleResponse])
async def get_roles(db:AsyncSession=Depends(getdb)):
    """获取所有提角色"""
    service=RoleService(db)

    try:
        roles=await service.get_all()
        return roles
    except Exception as e:
         raise HTTPException(status_code=500,
                             detail=f"获取提角色列表失败{str(e)}"
                             )

@router.get("/{Role_id}",response_model=RoleResponse)
async def get_role(role_id:int,db:AsyncSession=Depends(getdb)):
    service=RoleService(db)

    role=await service.get_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404,detail=f"提角色{str(role_id)}不存在")
    return role


@router.put("/{Role_id}",response_model=RoleResponse)
async def update_role(
        role_id:int,
        prover_data:RoleUpdate,
        db:AsyncSession=Depends(getdb),
):
    service=RoleService(db)

    #如果更新名称，检查更新名称是否已经存在
    if prover_data.name:
        existing_role=await service.get_by_name(prover_data.name)
        if existing_role and existing_role.id!=role_id:
            raise HTTPException(
                status_code=400,
                detail=f"提角色名称‘{prover_data.name}’已经存在"
            )

    try:
        role=await service.update(role_id,prover_data)
        if not role:
            raise HTTPException(status_code=404,detail=f"提角色ID {role_id} 不存在")
        return role
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"更新失败{str(e)}")

@router.delete("/{role_id}",status_code=204)
async def delete_role(
        role_id:int,
        db:AsyncSession=Depends(getdb)):

    service=RoleService(db)

    try:
        success=await service.delete(role_id)
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"提角色 ID {role_id} 不存在"
                                )
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"删除提角色失败{str(e)}")





