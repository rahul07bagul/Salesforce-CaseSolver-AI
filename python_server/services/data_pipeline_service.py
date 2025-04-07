class DataPipelineService:
    def __init__(self, file_processor, mongo_db_handler, vector_database):
        self.file_processor = file_processor
        self.mongo_db_handler = mongo_db_handler
        self.vector_database = vector_database
        self.is_running = False
        print(f"DataPipelineService initialized with: {type(file_processor).__name__}, {type(mongo_db_handler).__name__}, {type(vector_database).__name__}")
        
    def process_files(self, file_path, file_type=None):
        if not self.is_running:
            raise RuntimeError("Pipeline is not running. Call run() first.")
        
        print(f"Starting to process files from: {file_path}")
        if file_type:
            print(f"File type specified: {file_type}")
        else:
            print("No file type specified, will auto-detect")
            
        processed_files = self.file_processor.process_file(file_path)
        print(f"Successfully processed {processed_files} files")
        
        print(f"All {processed_files} files stored successfully")    
        return processed_files
    
    def create_vector_embeddings(self, file_type=None):
        if not self.is_running:
            raise RuntimeError("Pipeline is not running. Call run() first.")
        
        print(f"Retrieving files of type '{file_type}' from document storage...")
        files = self.mongo_db_handler.get_files_by_type(file_type)
        print(f"Found {len(files)} files to process for vector embeddings")
        
        print("Creating vector embeddings...")
        for i, file in enumerate(files, 1):
            file_name = file.get('file_name', 'unknown')
            print(f"Processing file {i}/{len(files)}: {file_name}")
            
            content = file['content']
            metadata = {
                'file_name': file['file_name'],
                'source': file['metadata']['source'],
                'type': file['type']
            }
            
            self.vector_database.store_embeddings(content=content, metadatas=metadata)
            print(f"Embeddings stored successfully for file: {file_name}")
        
        print(f"Vector embeddings created for all {len(files)} files")
    
    def run(self):
        self.is_running = True
        print("Data pipeline started.")
    
    def stop(self):
        self.is_running = False
        print("Data pipeline stopped.")
        
    def run_complete_pipeline(self, file_path, file_type=None):
        print(f"Starting complete pipeline execution for file path: {file_path}")
        try:
            print("Step 0: Initializing pipeline...")
            self.run()
            
            print("Step 1: Processing files and storing in document database...")
            self.process_files(file_path, file_type)
            print("Step 1 completed successfully.")
            
            print("Step 2: Creating vector embeddings...")
            self.create_vector_embeddings(file_type)
            print("Step 2 completed successfully.")
            
            print("Pipeline execution completed successfully.")
            
        except Exception as e:
            print(f"Pipeline execution failed: {str(e)}")
            print(f"Error occurred at: {e.__traceback__.tb_lineno}")
        finally:
            print("Shutting down pipeline...")
            self.stop()