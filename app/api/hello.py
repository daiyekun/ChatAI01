# 从fastapi 库种导入 APIRouter 类，用于创建路由模块
from fastapi import  APIRouter

#创建一个APIRouter 的实例
#这就想asp.net core 种定义一个controller 类
router=APIRouter()

#使用装饰器定义一个api路由
#@router.post('/hello') 表示是一个处理http post 请求端点
@router.post('/hello')

#定义一个异步函数来处理这个请求
#函数名hello 是我们自己取的，它会线上再自动生成文档api 文档中
async def hellp():
    return 'Hello World!'