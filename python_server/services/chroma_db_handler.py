from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from models.openai_embedding_model import OpenAIEmbeddingModel
import os

class ChromaDBHandler:
    def __init__(self, base_dir='vector_db'):
        self.base_dir = base_dir
        self.embedding_model = OpenAIEmbeddingModel()
        self.init_vector_db()

    def init_vector_db(self):
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, exist_ok=True)

        self.db = Chroma(
            persist_directory=self.base_dir,
            embedding_function=self.embedding_model.embedding_model 
        )

    def create_chunks(self, text, chunk_size=1000, chunk_overlap=200):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks

    # if the text is too long, split it into chunks and store them separately
    def store_embeddings(self, chunks, metadatas):
        try:
            embeddings = [self.embedding_model.generate_embedding(chunk) for chunk in chunks]
            self.db.add_texts(texts=chunks, metadatas=metadatas, embeddings=embeddings)
            print("Embeddings stored successfully.")
        except Exception as e:
            raise RuntimeError(e)
    
    # if there are no chunks, store the text directly
    def store_embeddings(self, content, metadatas):
        try:
            embeddings = [self.embedding_model.generate_embedding(content)]
            self.db.add_texts(texts=[content], metadatas=[metadatas], embeddings=embeddings)
            print("Embeddings stored successfully.")
        except Exception as e:
            print(f"Error storing embeddings: {e}")
            raise RuntimeError(e)
    
    def search_embeddings(self, query, k=5):
        results = self.db.similarity_search(
            query,
            k
        )
        
        formatted_results = []
        for doc in results:
            formatted_results.append({
                'text': doc.page_content,
                'metadata': doc.metadata
            })
        
        return formatted_results