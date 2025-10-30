from typing import  List
from langchain_core.messages import  HumanMessage,AIMessage
from langchain_core.output_parsers import  StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import  ChatOpenAI
from app.data.models import  Role
from app.schemas.message import MessageBase, MessageRole
from langchain_core.prompts import  ChatPromptTemplate,MessagesPlaceholder


class AIChatService:
    def __init__(self,role:Role):
        #创建ChatOpenAI 实例
        llm=ChatOpenAI(
            base_url=role.provider.endpoint,
            api_key=role.provider.api_key,
            model=role.provider.model,
            temperature=role.temperature
        )

        #构造Prompt 模板

        prompt=ChatPromptTemplate.from_messages(
            [("system",role.system_prompt),
             MessagesPlaceholder(variable_name="history"),
             ("human","{input}")
             ] )

        #初始化输出解析器
        parser=StrOutputParser()

        #创建顺序链
        self.chain=prompt | llm |parser

    async def chat(self,history:List[MessageBase],user_input:str) -> str:
        # 转换历史信息
        chat_history=[
            HumanMessage(content=msg.content) if msg.role.value==MessageRole.User else AIMessage(content=msg.content)
            for msg in history if msg.role.value in (MessageRole.User, MessageRole.Assistant)
        ]

        #调用链
        result=await  self.chain.ainvoke({"history":chat_history,"input":user_input})
        return  result


