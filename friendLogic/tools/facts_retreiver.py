from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser

from pydantic import BaseModel, Field

from friendLogic.prompts.tools_prompts import facts_keys_retriever_prompts
from knowledger.vectorstore.hybrid_store import MilvusStoreWithClient

import os
from dotenv import load_dotenv
load_dotenv()

class Retreived(BaseModel):
    retreived_things: list[str] = Field(description="List of retreived things")

class FactsRetriever:
    fact_keys_prompt = facts_keys_retriever_prompts
    llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"])
    vectorstore = MilvusStoreWithClient()
    parser =  JsonOutputParser(pydantic_object=Retreived) 

    @classmethod
    def key_intention_retriever(cls, message:str):

        runnable = cls.fact_keys_prompt | cls.llm | JsonOutputParser(pydantic_object=Retreived)
        result = runnable.invoke({"message": message, "format_instructions": cls.parser.get_format_instructions()})
        print("Result: ", result["retreived_things"])   
        #Retrieve facts from vectorstore databasejmj
        retrieved_facts = cls.vectorstore.hybrid_search(collection_name="test", query=result["retreived_things"][0],fixed_filter=None, output_fields=None)
        print("Result retrieved: ",retrieved_facts)   

        return result["retreived_things"]

    @staticmethod
    @tool
    def retrieve_facts(message:str):
        """Fetch relevant information about your friends life, facts about him and his friends or current user interaction to. Containing information about his family, friend, work, hobbies, events etc.
        Use this when need information about user's life and his past events. 
        Use this when need facts about user, personal information about user or his closest people.

         Args:
            message (string): Exact message from the user, not changed message.

        Returns:
            A list of strings containing relevant information about user's life and his past events.
        """
        print("Start facts retriever from: ", message)
        facts = FactsRetriever.key_intention_retriever(message)
        #TODO Retrieve facts from the user from vectorstore database

        return facts