import os
import PyPDF2
import json

class DocumentProcessor:
    def __init__(self, mongodb_handler=None):
        self.mongodb_handler = mongodb_handler
        self.supported_extensions = {
            '.pdf': self._process_pdf,
            '.json': self._process_json,
        }
        
    def process_directory(self, directory_path, max_file_size_mb=10):
        total_documents = 0
        
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_extension = os.path.splitext(file_path)[1].lower()
                
                if file_extension in self.supported_extensions:
                    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                    
                    # Process file based on its extension
                    processor = self.supported_extensions[file_extension]
                    document_chunks = processor(file_path, max_file_size_mb)
                    
                    # Save each chunk to MongoDB
                    for chunk in document_chunks:
                        try:
                            self.mongodb_handler.insert_file(chunk)
                        except Exception as e:
                            print(f"Error saving file {chunk['file_name']}: {e}")
                    
                    total_documents += len(document_chunks)
        
        return total_documents
    
    def process_file(self, file_path, max_file_size_mb=10):
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension in self.supported_extensions:
            processor = self.supported_extensions[file_extension]
            document_chunks = processor(file_path, max_file_size_mb)
            
            # Save each chunk to MongoDB
            for chunk in document_chunks:
                try:
                    self.mongodb_handler.insert_file(chunk)
                except Exception as e:
                    print(f"Error saving file {chunk['file_name']}: {e}")
            
            return len(document_chunks)
        else:
            print(f"Unsupported file type: {file_extension}")
            return 0

    def _process_pdf(self, file_path, max_file_size_mb=10):
        document_chunks = []
        file_name = os.path.basename(file_path)
        
        # Check file size to determine approach
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        
        if file_size_mb > max_file_size_mb:
            # Process large PDF by pages or sections
            return self._process_large_pdf(file_path, max_file_size_mb)
        else:
            # Process smaller PDF as a whole
            text = self._extract_text_from_pdf(file_path)
            
            if text.strip():
                document = {
                    'file_name': file_name,
                    'content': text,
                    'source': file_path,
                    'type': 'pdf'
                }
                document_chunks.append(document)
            
        return document_chunks
    
    def _process_large_pdf(self, file_path, max_file_size_mb):
        document_chunks = []
        file_name = os.path.basename(file_path)
        
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            
            # Estimate pages per section based on file size and max size
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            pages_per_section = max(1, int(total_pages * max_file_size_mb / file_size_mb))
            
            # Process PDF in sections
            for start_page in range(0, total_pages, pages_per_section):
                end_page = min(start_page + pages_per_section, total_pages)
                chunk_number = (start_page // pages_per_section) + 1
                
                # Extract text from page range
                section_text = ""
                for page_num in range(start_page, end_page):
                    page = reader.pages[page_num]
                    section_text += page.extract_text() or ""
                
                if section_text.strip():
                    # Create document chunk with simplified naming
                    chunk_file_name = f"{os.path.splitext(file_name)[0]}_chunk_{chunk_number}{os.path.splitext(file_name)[1]}"
                    
                    document = {
                        'file_name': chunk_file_name,
                        'content': section_text,
                        'source': file_path,
                        'type': 'pdf',
                        'page_start': start_page,
                        'page_end': end_page,
                        'total_pages': total_pages
                    }
                    
                    document_chunks.append(document)
        
        return document_chunks
    
    def _extract_text_from_pdf(self, file_path):
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    def _process_json(self, file_path, max_file_size_mb=0):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            
            documents = []
            for article in articles:
                if isinstance(article, dict):
                    document = {
                        'file_name': os.path.basename(file_path),
                        'content': article['text'],
                        'source': file_path,
                        'metadata': article['metadata'],
                        'type': 'json',
                    }
                    documents.append(document)

            return documents
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON file {file_path}: {e}")
            return []
        except Exception as e:
            print(f"Error processing JSON file {file_path}: {e}")
            return []

# # Usage example:
# def process_documents(data_folder):
#     processor = DocumentProcessor()
#     total_chunks = processor.process_directory(data_folder)
#     print(f"Created {total_chunks} document chunks from files in {data_folder}")
    
# # Entry point
# if __name__ == "__main__":
#     data_folder = "../data"
#     process_documents(data_folder)