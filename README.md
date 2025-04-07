# Salesforce Case Resolver with AI and RAG

An intelligent case resolution system for Salesforce that leverages AI and Retrieval Augmented Generation (RAG) to provide solutions based on your knowledge articles.

<p align="center">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/ChromaDB-9B59B6?style=for-the-badge&logo=chromadb&logoColor=white" alt="ChromaDB">
  <img src="https://img.shields.io/badge/Salesforce-00A1E0?style=for-the-badge&logo=salesforce&logoColor=white" alt="Salesforce">
  <img src="https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI">
  <img src="https://img.shields.io/badge/google%20gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white" alt="Gemini">
</p>

## Overview
This application connects your Salesforce instance with an AI-powered backend that:
1. Receives case data from Salesforce
2. Uses a RAG-based approach to find relevant information in your knowledge base
3. Generates comprehensive solutions using AI (Gemini model)
4. Returns formatted HTML solutions directly to your Salesforce interface

The system uses ChromaDB as a vector database and OpenAI embeddings to effectively retrieve contextually relevant information from your knowledge articles.

## Demo
![Design](https://github.com/rahul07bagul/Salesforce-CaseSolver-AI/blob/main/assets/demo.gif)

## Architecture
![Design](https://github.com/rahul07bagul/Salesforce-CaseSolver-AI/blob/main/assets/sfdc_case_resolver_design.png)

## Demo Implementation
The current implementation demonstrates the system using:
- Knowledge articles scraped from Purdue University
- Vector embeddings stored in ChromaDB
- Flask server for API endpoints
- LWC component integration in Salesforce

## Architecture
```bash
┌─────────────┐     ┌───────────────┐     ┌──────────────────┐
│  Salesforce │     │ Flask Server  │     │  Vector Database │
│  LWC        │────▶│ /get_resolution│────▶│  (ChromaDB)      │
│  Component  │◀────│               │◀────│                  │
└─────────────┘     └───────────────┘     └──────────────────┘
                            │                      ▲
                            ▼                      │
                    ┌──────────────┐       ┌──────────────┐
                    │ AI Model     │       │ Knowledge    │
                    │ (Gemini)     │       │ Articles     │
                    └──────────────┘       └──────────────┘
```
## Installation
Prerequisites
- Python 3.8+
- OpenAI API Key
- Google Gemini API Key
- MongoDB
- ngrok (for local development testing)

## Backend Setup
1. Setup
```bash
git clone [your-repository-url]
cd python_server
pip install -r requirements.txt
```
2. Create .env file with below content and add your API keys
```bash
GEMINI_API_KEY=""
GEMINI_MODEL_NAME="gemini-2.0-flash"
GEMINI_EMBEDDING_MODEL_NAME="gemini-embedding-exp-03-07"
OPENAI_API_KEY=
OPENAI_EMBEDDING_MODEL_NAME="text-embedding-3-small"
MONGODB_URI="mongodb://localhost:27017/"
MONGODB_DB_NAME="SFDC_AI"
CURRENT_MODEL="Gemini"
```
3. Process knowledge articles (one-time setup):
```bash
python run_pipeline.py
```
This will:
- Process the sample Purdue articles (from the provided JSON file)
- Store them in MongoDB
- Create vector embeddings in ChromaDB
4. Start the Flask server:
```bash
python app.py
```
5. For local development, expose your server using ngrok:
  ```bash
  ngrok http 5000
  ```

## Salesforce Setup
1. Add the ngrok URL to Salesforce Trusted Sites:
    - Setup > Trusted URL > New
    - Add the ngrok URL (or your production server URL)
2. Create a Custom Label for your endpoint:
    - Setup > Custom Labels > New
    - Create a new label (e.g., "Python_App_URL")
    - Set the value to your server URL + "api/v1/cases/get_resolution"
3. Deploy the LWC component:
    - Use the LWC component code provided in the repository
    - Update the API endpoint reference to use your Custom Label
4. Add the LWC component to the Case Record Page:
    - Setup > Object Manager > Case
    - Lightning Record Pages > Case Record Page
    - Edit layout and add your component

## Usage
1. Open a Case in Salesforce
2. Click the "Get Resolution" button in your LWC component
3. The system will:
   - Send case data to your Flask server
   - Process the case using RAG and AI
   - Return a formatted solution
   - Display the solution in the Salesforce interface


