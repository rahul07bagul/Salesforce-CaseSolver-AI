from dotenv import load_dotenv
import os

class ModelFactory:
    def __init__(self, system_prompt):
        load_dotenv()
        self.model_name = os.getenv("CURRENT_MODEL")
        self.system_prompt = system_prompt
        if not self.model_name:
            raise ValueError("Model name not specified in environment variables.")

    def create_model(self):
        if self.model_name == "Gemini":
            from models.gemini_model import GeminiModel
            return GeminiModel(self.system_prompt)
        else:
            raise ValueError(f"Model {self.model_name} is not supported.")