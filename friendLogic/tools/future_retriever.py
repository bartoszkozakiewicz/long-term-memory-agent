from langchain_core.tools import tool

class FutureRetriever:
    def __init__(self) -> None:
        pass

    @staticmethod
    @tool
    def future_retriever(self):
        """Fetch relevant information about your friends future plans only. Use this when user is asking about some future events that he planned. For example some future events, trips, meetings, etc.

        Returns:
            A list of strings containing relevant information about user's planned events etc.
        """
        
        print("Retrieving user's future plans")
        #TODO Retrieve future plans from the user from vectorstore database
        return "Future plans retrieved"