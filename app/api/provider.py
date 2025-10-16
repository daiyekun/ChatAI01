from email.policy import default

from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import  AsyncSession
from app.data.db import  getdb
from app.schemas.provider import ProviderResponse, ProviderCreate, ProviderUpdate
from app.service.provider import ProviderService

from typing import  List

router=APIRouter(prefix= "/providers",tags=["模型提供商管理"])

@router.post("/",response_model=ProviderResponse,status_code=201 )
async  def create_provider(prover_data:ProviderCreate,db:AsyncSession=Depends(getdb)):
    """创建新的模型提供商"""
    service=ProviderService(db)

    try:
        provider=await service.create(prover_data)
        return  provider
    except Exception as e:
        raise  HTTPException(status_code=500,detail=f"模型提供商创建失败{str(e)}")


@router.get("/",response_model=List[ProviderResponse])
async def list_providers(db:AsyncSession=Depends(getdb)):
    """获取所有提供商"""
    service=ProviderService(db)

    try:
        providers=await service.get_all()
        return providers
    except Exception as e:
         raise HTTPException(status_code=500,
                             detail=f"获取提供商列表失败{str(e)}"
                             )

@router.get("/{provider_id}",response_model=ProviderResponse)
async def get_provider(provider_id:int,db:AsyncSession=Depends(getdb)):
    service=ProviderService(db)

    provider=await service.get_by_id(provider_id)
    if not provider:
        raise HTTPException(status_code=404,detail=f"提供商{str(provider_id)}不存在")
    return provider


@router.put("/{provider_id}",response_model=ProviderResponse)
async def update_provider(
        provider_id:int,
        prover_data:ProviderUpdate,
        db:AsyncSession=Depends(getdb),
):
    service=ProviderService(db)

    #如果更新名称，检查更新名称是否已经存在
    if prover_data.name:
        existing_provider=await service.get_by_name(prover_data.name)
        if existing_provider and existing_provider.id!=provider_id:
            raise HTTPException(
                status_code=400,
                detail=f"提供商名称‘{prover_data.name}’已经存在"
            )

    try:
        provider=await service.update(provider_id,prover_data)
        if not provider:
            raise HTTPException(status_code=404,detail=f"提供商ID {provider_id} 不存在")
        return provider
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"更新失败{str(e)}")

@router.delete("/{provider_id}",status_code=204)
async def delete_provider(
        provider_id:int,
        db:AsyncSession=Depends(getdb)):

    service=ProviderService(db)

    try:
        success=await service.delete(provider_id)
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"提供商 ID {provider_id} 不存在"
                                )
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"删除提供商失败{str(e)}")





