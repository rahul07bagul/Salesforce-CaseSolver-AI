from pymongo import MongoClient
import os
from dotenv import load_dotenv
import re

class MongoDBHandler:
    def __init__(self):
        load_dotenv()
        self.uri = os.getenv("MONGODB_URI")
        self.db_name = os.getenv("MONGODB_DB_NAME")
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
    
    def insert_file(self, file_data):
        try:
            self.db.files.insert_one(file_data)
        except Exception as e:
            raise Exception(f"Error saving file: {e}")
    
    def get_files(self):
        try:
            files = list(self.db.files.find())
            return files
        except Exception as e:
            raise Exception(f"Error retrieving files: {e}")
    
    def get_files_by_type(self, file_type):
        try:
            files = list(self.db.files.find({"type": file_type}))
            return files
        except Exception as e:
            raise Exception(f"Error retrieving files: {e}")