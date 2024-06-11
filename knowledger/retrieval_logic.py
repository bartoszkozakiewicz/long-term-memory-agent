from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser


from knowledger.sql_database.sql_manipulations import SQLDatabase
from knowledger.vectorstore.vs_manipulations import VectorStoreManipulations

import os
from dotenv import load_dotenv
load_dotenv()

class RetrievalKnowledgeLogic:
    ''' Initial version of the class, which will be responsible for the logic of the knowledge logic, which is retrieval process, but also inserint and updating.'''
    llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"])


    # ================== RETRIEVEAL OF FACTS ABOUT PEOPLE ==================
    @staticmethod
    def select_people_facts( 
                    first_name:Optional[str]=None, 
                    last_name:Optional[str]=None, 
                    called:Optional[str]=None, 
                    gender:Optional[str]=None,
                    category:Optional[str]=None,
                    query:Optional[str]=None):
        '''In the future category probably will be a list of categories, but for now it is a string.'''
        
        if category == "basic":
            ''' W takim przypadku wyciągamy właśnie podstawowe informacje o osobie, takie jak imię, nazwisko, pseudonim, opis, data urodzenia, wiek, płeć.'''
            SQLDatabase._select_basic_info(first_name, last_name, called, gender)

        else:
            ''' W przeciwnym wypadku wyciągamy informacje - fakty etc z vectorstore.'''
            VectorStoreManipulations.facts_vs_retrieval(query, category)

    
    # ================== RETRIEVEAL OF PEOPLE RELATIONSHIPS ==================
    @classmethod
    def relationships_retrieval(cls, person1_name:Optional[str]=None, person2_name:Optional[str]=None, type:Optional[str]=None) -> list[dict]:
        retrieved_facts = SQLDatabase.select_relationship_info(person1_name, person2_name, type)
        print("Events retrieved: ",retrieved_facts)   
        return retrieved_facts

    # ================== RETRIEVEAL OF PEOPLE PAST EVENTS DATA ==================
    @classmethod
    def events_vs_retrieval(cls, query:str, people:list[str]) -> list[dict]:
        retrieved_events = VectorStoreManipulations.events_vs_retrieval(query, people)
        print("Events retrieved: ",retrieved_events)   
        return retrieved_events
    
    # ================== RETRIEVEAL OF PEOPLE FUTURE EVENTS DATA ==================
    @classmethod
    def future_events_vs_retrieval(cls, query:str, people:list[str]) -> list[dict]:
        retrieved_events = VectorStoreManipulations.future_events_vs_retrieval(query, people)
        print("Events retrieved: ",retrieved_events)   
        return retrieved_events