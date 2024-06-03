
from  langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import os 
from dotenv import load_dotenv
load_dotenv()

class Agent:
    def __init__(self,tools,prompt:ChatPromptTemplate):
        self.tools = tools
        self.prompt = prompt
        self.llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"])
        self.runnable = self.prompt | self.llm.bind_tools(tools)

    def __call__(self, state):
        # print("State in main agent: ",state)
        last_message = state["messages"]
        
        result = self.runnable.invoke(state)
        print("Result in main agent: ",result)
        return {"messages": result}