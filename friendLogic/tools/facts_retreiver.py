from langchain_core.tools import tool

class FactsRetriever:
    def __init__(self):
        pass

    @staticmethod
    @tool
    def retrieve_facts():
        """Fetch relevant information about your friends life, facts about him and his friends or current user interaction to. Containing information about his family, friend, work, hobbies, events etc.
        Use this when need information about user's life and his past events. 
        Use this when need facts about user, personal information about user or his closest people.

        Returns:
            A list of strings containing relevant information about user's life and his past events.
        """
        
        #TODO Retrieve facts from the user from vectorstore database

        return "Facts retrieved" 