from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from models.embedding_model import EmbeddingModel

class GeminiEmbeddingModel(EmbeddingModel):
    def __init__(self):
        load_dotenv()
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.GEMINI_MODEL_NAME = os.getenv("GEMINI_EMBEDDING_MODEL_NAME")
        self.client = genai.Client(api_key=self.GEMINI_API_KEY)
        
    def generate_embedding(self, contents):
        result = self.client.models.embed_content(
            model=self.GEMINI_MODEL_NAME,
            contents=contents,
            config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
        )
        return result.embeddings