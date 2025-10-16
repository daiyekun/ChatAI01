from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import  AsyncSession
from app.data.db import  getdb
from app.schemas.provider import ProviderResponse,ProviderCreate
from app.service.provider import ProviderService

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
