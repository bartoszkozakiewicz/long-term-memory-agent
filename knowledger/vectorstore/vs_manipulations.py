from knowledger.vectorstore.hybrid_store import MilvusStoreWithClient


class VectorStoreManipulations:
    vectorstore = MilvusStoreWithClient()

    # ================== RETRIEVEAL OF PEOPLE FACTS AND RELATIONSHIPS DATA ==================
    @classmethod
    def facts_vs_retrieval(cls, query:str, category:str) -> list[dict]:
        retrieved_facts = cls.vectorstore.hybrid_search(collection_name="facts_collection", query=query,fixed_filter=f"category == '{category}'", output_fields=None)
        print("Result retrieved: ",retrieved_facts)   
        return retrieved_facts
    
     # ================== RETRIEVEAL OF PEOPLE PAST EVENTS DATA ==================
    @classmethod
    def events_vs_retrieval(cls, query:str, people:list[str]) -> list[dict]:    
        retrieved_events = cls.vectorstore.hybrid_search(collection_name="past_events_collection", query=query,fixed_filter=f"TODO", output_fields=None)
        print("Events retrieved: ",retrieved_events)   
        return retrieved_events
    
    # ================== RETRIEVEAL OF PEOPLE FUTURE EVENTS DATA ==================
    @classmethod
    def future_events_vs_retrieval(cls, query:str, people:list[str]) -> list[dict]:
        retrieved_events = cls.vectorstore.hybrid_search(collection_name="future_events_collection", query=query,fixed_filter=f"TODO", output_fields=None)
        print("Events retrieved: ",retrieved_events)   
        return retrieved_events
    

    # ================== UPDATING DATABASE =====================
    

    # ================== INSERT INTO DATABASE ==================
