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
