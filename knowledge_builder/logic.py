from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser


from knowledge_builder.sql_database.sql_manipulations import SQLDatabase
from knowledge_builder.vectorstore.hybrid_store import MilvusStoreWithClient

import os
from dotenv import load_dotenv
load_dotenv()

class KnowledgeLogic:
    ''' Initial version of the class, which will be responsible for the logic of the knowledge logic, which is retrieval process, but also inserint and updating.'''

    llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"])
    vectorstore = MilvusStoreWithClient()

    # ================== RETRIEVEAL OF PEOPLE FACTS AND RELATIONSHIPS DATA ==================
    @classmethod
    def facts_vs_retrieval(cls, query:str, category:str) -> list[dict]:
        retrieved_facts = cls.vectorstore.hybrid_search(collection_name="test", query=query,fixed_filter=f"category == '{category}'", output_fields=None)
        print("Result retrieved: ",retrieved_facts)   

        return retrieved_facts

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
            KnowledgeLogic.facts_vs_retrieval(query, category)

    
    # ================== RETRIEVEAL OF PEOPLE PAST EVENTS DATA ==================
    @classmethod
    def events_vs_retrieval(cls, query:str, category:str) -> list[dict]:
        #TODO: Change the collection name to the proper one (Firstly create proper vectorstore, pipeline etc.)
        #TODO: Add the fixed filters -> other args
        retrieved_facts = cls.vectorstore.hybrid_search(collection_name="database-with-events", query=query,fixed_filter=None, output_fields=None)
        print("Events retrieved: ",retrieved_facts)   

        return retrieved_facts