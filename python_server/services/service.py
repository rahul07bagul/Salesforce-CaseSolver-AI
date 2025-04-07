from services import mongo_db_handler, chroma_db_handler, file_processor
from models.model_factory import ModelFactory
from services.prompt_service import get_system_prompt
from services.data_pipeline_service import DataPipelineService

class Service:
    def __init__(self):
        self.mongo_db_handler = mongo_db_handler.MongoDBHandler()
        self.file_processor = file_processor.DocumentProcessor(mongodb_handler=self.mongo_db_handler)
        self.chroma_db_handler = chroma_db_handler.ChromaDBHandler()
        self.model = ModelFactory(system_prompt=get_system_prompt()).create_model()
    
    def get_resolution(self, case):
        context = self.chroma_db_handler.search_embeddings(case.body, k=5)
        prompt = self.create_prompt(case, context)
        return self.model.generate_content(prompt)

    def create_prompt(self, case, context):
        prompt = f"""
        Below are the details of the case and the context:

        Case ID: {case.case_id}
        Subject: {case.subject}
        Body: {case.body}
        Knowledge Articles (context): {context}
        """
        return prompt

    def run_data_pipeline(self, file_path, file_type=None):
        data_pipeline_service = DataPipelineService(
            file_processor=self.file_processor,
            mongo_db_handler=self.mongo_db_handler,
            vector_database=self.chroma_db_handler
        )
        return data_pipeline_service.run_complete_pipeline(file_path, file_type)
