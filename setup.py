# setup.py
from setuptools import setup, find_packages

setup(
    name="rbac-main",
    version="0.1.0",
    packages=find_packages(include=['app', 'app.*']),
    install_requires=[
        # Web framework
        "fastapi[standard]>=0.115.12",
        "uvicorn[standard]>=0.21.1",

        # LangChain embeddings & vectorstore
        "langchain-huggingface>=0.2.0",
        "langchain-chroma>=0.2.4",

        # Core vector DB & models
        "chromadb>=1.0.12",
        "sentence-transformers>=2.2.2",
        "torch>=2.1.0",

        # Auth / security
        "python-jose[cryptography]",
        "passlib[bcrypt]",

        # Env & HTTP
        "python-dotenv",
        "requests>=2.28.1,<3.0.0",

        # Utility
        "tabulate",
    ],
    python_requires=">=3.9",
)
