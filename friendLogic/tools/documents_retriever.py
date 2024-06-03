from langchain_core.tools import tool


class DocumentsRetriever:
    def __init__(self) -> None:
        pass

    @staticmethod
    @tool
    def retrieve_documents():
        """Fetch relevant information about your friends documents that your friend uploaded for you in the past. Use this when user is asking about some informations from document that he uploaded. For example from some pdf, docx ...

        Returns:
            A list of strings containing relevant information retrieved from user's documents.
        """
        print("Retrieving documents from user's documents")
        # TODO: Retrieve documents from the user from vectorstore database

        return "Documents retrieved, there are 3 countries in the world."