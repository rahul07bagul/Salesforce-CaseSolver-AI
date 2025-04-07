from dotenv import load_dotenv
import os
from openai import OpenAI
from models.embedding_model import EmbeddingModel 
from langchain_openai import OpenAIEmbeddings

class OpenAIEmbeddingModel(EmbeddingModel):
    def __init__(self):
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.OPENAI_MODEL_NAME = os.getenv("OPENAI_EMBEDDING_MODEL_NAME")
        self.embedding_model = OpenAIEmbeddings()
    
    def generate_embedding(self, contents):
        return self.embedding_model.embed_query(contents)