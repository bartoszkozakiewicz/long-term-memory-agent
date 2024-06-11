from langchain_openai import OpenAIEmbeddings
import os 
from dotenv import load_dotenv
load_dotenv()

class EmbeddingGenerator:
    """Generates embeddings for textual data."""

    def __init__(self, dimension=1536):
        self.dimension = dimension
        self.emebeding_model = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    

    def generate(self, text):
        """Generates an embedding for the text."""
        return self.emebeding_model.embed_query(text=text)
