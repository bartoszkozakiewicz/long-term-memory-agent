from langgraph.graph import StateGraph, END
from langgraph.prebuilt import tools_condition
from langgraph.graph.message import AnyMessage, add_messages


from typing import Annotated, TypedDict, Literal
from pydantic import BaseModel, Field

from friendLogic.agents.friend_agent import Agent
from friendLogic.prompts.prompts import main_agent_prompt
from friendLogic.tools import *
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

class BasicUserInfo(TypedDict):
    name: str
    surname: str
    age: str
    current_partner: str
    current_work: str
    current_location: str


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    friends_family: Annotated[list[str], add_messages] # list of names of friends and family
    basic_user_info: BasicUserInfo # dictionary containing basic user information like name, surname, age, current_partner, current_work, current_location
    weekly_events: Annotated[list[str], add_messages] #List of important events from last week

class talkGraph:
    def __init__(self):
        self.facts_retriever = FactsRetriever()
        self.documents_retriever = DocumentsRetriever()
        self.future_retriever = FutureRetriever()
        self.tools = [self.facts_retriever.retrieve_facts,  self.documents_retriever.retrieve_documents, self.future_retriever.future_retriever]

        self.agent = Agent(tools=self.tools, prompt=main_agent_prompt)

    def where_main_agent_go(self,state):
        route = tools_condition(state)
        print("Route: ", route)
        if route == END:
            return END
        
        last_tool_calls = state["messages"][-1].tool_calls
        print("Last tool calls: ", last_tool_calls)

        return "memory retriever"


    def builder(self):
        graph = StateGraph(State)
        graph.add_node("main_agent",self.agent)
        graph.set_entry_point("main_agent")

        graph.add_node("memory_retriever",tools_node_with_fallback(self.tools))

        graph.add_conditional_edges(
            "main_agent",
            self.where_main_agent_go,
            {
                "memory retriever":"memory_retriever",
                END:END
            }
        )

        graph.add_edge("memory_retriever","main_agent")

        return graph.compile(checkpointer=SqliteSaver.from_conn_string("checkpoints.sqlite"))