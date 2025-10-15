# ChatAI01
用于学习AI应用开发


uv 安装文档
https://docs.astral.sh/uv/getting-started/installation/#next-steps


依赖环境恢复
```shell
uv sync 
```

#初始化迁移
```shell
alembic init alembic 
```

#未来结构改变以后重复执行以下两个脚本
#生成迁移脚本--执行前先手动建立库
```shell
alembic revision --autogenerate -m "Initial migration"
```


#应用迁移 把升级脚本执行到数据库
```shell
alembic upgrade head
```
