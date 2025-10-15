#从fastapi 库导入FastAPI类，这是创建应用核心
from importlib import reload

from fastapi import  FastAPI
#从我们创建的api 字目录导入hello 模板（hello.py文件）
from api import  hello

#创建一个fasetAPI 应用的实例
#类似program.cs中调用WebApplication.CreateBuilder() 和bulider.Bulid()

app=FastAPI(
    #title 是一个可选参数 ，它会线上再自动生成api文档位置
    title="AI 聊天平台测试",
    # version 是办不办好，同样会线上在文档中
    version="1.0",
)

#使用app.include_router() 方法类将我们创建的角色路由包含到引用中
#这里雷士在asp.net core 中调用app.MapControllers()

app.include_router(
    #第一个参数是我们想要包含的路由对象
    hello.router,
#prefix 参数魏我们路由端点添加一个前缀
#这样我们的hello.py 中 "/hello" 就会变成 “/api/hello”
    prefix="/api",
    #tags 参数用于在api 文档中对端点进行分组
    #所有来治愈roles.router 端点都会被归类 “测试" 这个标签下
    tags=["测试"]
)

#定义一个根路径get 请求处理函数
#这样通常用于检查服务器是否正常

@app.get("/")
async def read_root():
    return {"message": "还原使用通用ai聊天平台"}

if __name__ == "__main__":
    import uvicorn
    #使用uvicorn 运行当前应用，指定应用路径，主机地址，端口和热加载功能
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000,reload=True)