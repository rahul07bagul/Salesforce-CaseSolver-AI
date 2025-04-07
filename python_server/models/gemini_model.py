from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from models.model import Model

class GeminiModel(Model):    
    def __init__(self, system_prompt):
        load_dotenv()
        self.system_prompt = system_prompt
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.MODEL_NAME = os.getenv("GEMINI_MODEL_NAME")
        self.client = genai.Client(api_key=self.GEMINI_API_KEY)
    
    def generate_content(self, contents):
        response = self.client.models.generate_content(
            model=self.MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt),
            contents=contents,
        )
        return response.text