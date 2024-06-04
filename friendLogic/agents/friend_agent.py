
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
        print("STAN: ", state)

        
        result = self.runnable.invoke(state)

        if not state["basic_user_info"]:
            basic_user_info = {
                "name": "",
                "surname": "",
                "age": "",
                "current_partner": "",
                "current_work": "",
                "current_location": ""
            }
            return {"messages": result, "basic_user_info": basic_user_info}

        return {"messages": result}