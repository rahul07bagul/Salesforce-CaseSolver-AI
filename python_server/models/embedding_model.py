from abc import ABC, abstractmethod
import os

class EmbeddingModel(ABC):
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'vectorDB', 'chroma_db'))

    @abstractmethod
    def generate_embedding(self, contents):
        pass