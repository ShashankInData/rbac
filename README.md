HEAD
# RBAC Chatbot with Document Ingestion

A Role-Based Access Control (RBAC) chatbot system with document ingestion, semantic search, and a modern Streamlit frontend.

## Features

- 🔐 **Role-Based Access Control**: Different access levels for different user roles
- 📄 **Document Ingestion**: Load and process markdown/text documents
- 🔍 **Semantic Search**: Vector-based document retrieval using ChromaDB
- 🤖 **AI Chat**: Powered by Groq LLM API for intelligent responses
- 🎨 **Modern UI**: Beautiful Streamlit frontend with banner image
- 🔒 **Authentication**: JWT-based authentication system

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file with your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Ingest Documents
```bash
python scripts/ingest.py
```

### 4. Start the Application
```bash
python start_servers.py
```

This will start both the FastAPI backend and Streamlit frontend.

## Access Points

- **Frontend**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## User Roles

- **Engineering**: Access to technical documentation
- **Finance**: Access to financial reports
- **HR**: Access to employee policies
- **Marketing**: Access to marketing materials

## Default Credentials

- Username: `Tony`
- Password: `password123`
- Role: Engineering

## Architecture

- **Backend**: FastAPI with JWT authentication
- **Frontend**: Streamlit with modern UI
- **Vector Store**: ChromaDB with HuggingFace embeddings
- **LLM**: Groq API for response generation
- **RBAC**: Role-based document access control
=======
# DS RPC 01: Internal chatbot with role based access control

This is the starter repository for Codebasics's [Resume Project Challenge](https://codebasics.io/challenge/codebasics-gen-ai-data-science-resume-project-challenge) of building a RAG based Internal Chatbot with role based access control. Please fork this repository to get started.

Basic Authentication using FastAPI's `HTTPBasic` has been implemented in `main.py` for learners to get started with.

Visit the challenge page to learn more: [DS RPC-01](https://codebasics.io/challenge/codebasics-gen-ai-data-science-resume-project-challenge)
![alt text](resources/RPC_01_Thumbnail.jpg)
### Roles Provided
 - **engineering**
 - **finance**
 - **general**
 - **hr**
 - **marketing**

