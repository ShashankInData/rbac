import os
import sys
from pathlib import Path
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.core.settings import get_settings
from app.core.roles import DEPARTMENT_DIRS
import hashlib
import chromadb
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Adding the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

settings = get_settings()

def load_documents() -> List[Dict]:
    """Load and process documents from the resources/data directory."""
    documents = []
    base_path = project_root / "resources" / "data"
    logging.info(f"Looking for documents in: {base_path}")
    
    # Department mapping based on filename patterns
    def get_department_from_filename(filename: str) -> str:
        filename_lower = filename.lower()
        if "engineering" in filename_lower:
            return "engineering"
        elif "financial" in filename_lower or "finance" in filename_lower:
            return "finance"
        elif "hr" in filename_lower or "employee" in filename_lower:
            return "hr"
        elif "marketing" in filename_lower or "market" in filename_lower:
            return "marketing"
        else:
            return "general"
    
    # Look for both .txt and .md files directly in the data directory
    for file_path in base_path.glob("*.*"):
        if file_path.suffix.lower() in ['.txt', '.md']:
            logging.info(f"Found file: {file_path}")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    filename = file_path.name
                    department = get_department_from_filename(filename)
                    documents.append({
                        "content": content,
                        "metadata": {
                            "source": str(file_path.relative_to(base_path)),
                            "department": department
                        }
                    })
                logging.info(f"Successfully loaded {file_path} (department: {department})")
            except Exception as e:
                logging.error(f"Error loading {file_path}: {str(e)}")
    
    logging.info(f"Total documents loaded: {len(documents)}")
    return documents

def chunk_hash(text, metadata):
    """Generate a SHA256 hash for a chunk based on its text and metadata."""
    hash_input = text + str(metadata)
    return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()

def main():
    # Load documents
    documents = load_documents()
    logging.info(f"Total documents found: {len(documents)}")
    for doc in documents:
        logging.info(f"Source: {doc['metadata']['source']}")

    # Process all documents (no filter)
    logging.info(f"Processing {len(documents)} document(s)")
    
    # Initialize embeddings and vector store
    try:
        logging.info("Initializing HuggingFace embeddings...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        logging.info("HuggingFace embeddings initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing HuggingFace embeddings: {e}")
        raise

    try:
        logging.info("Initializing Chroma vector store...")
        # Create a new collection
        client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)
        collection = client.get_or_create_collection(
            name="rbac",
            metadata={"hnsw:space": "cosine"}
        )
        logging.info("Chroma vector store initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing Chroma vector store: {e}")
        raise
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,  # Increased from 1000 for more context
        chunk_overlap=300,  # Increased from 200 for better context continuity
        length_function=len,
        is_separator_regex=False,
        separators=["\n\n", "\n", ". ", " ", ""]  # Better separators for more natural chunks
    )
    
    # Process and store documents
    BATCH_SIZE = 10  # Reduced batch size for testing

    total_chunks = 0
    for doc in documents:
        chunks = text_splitter.split_text(doc["content"])
        logging.info(f"{doc['metadata']['source']}: {len(chunks)} chunks")
        batch_texts = []
        batch_metas = []
        for i, chunk in enumerate(chunks):
            if i >= BATCH_SIZE:
                break
            meta = doc["metadata"].copy()
            batch_texts.append(chunk)
            batch_metas.append(meta)
        try:
            logging.info("About to add batch to vector store...")
            if batch_texts:
                logging.info(f"Processing batch of {len(batch_texts)} chunks...")
                try:
                    # Test embedding a single chunk first
                    logging.info("Testing embedding on a single chunk...")
                    test_embedding = embeddings.embed_query(batch_texts[0])
                    logging.info(f"Successfully embedded test chunk. Vector size: {len(test_embedding)}")
                    
                    logging.info("Adding batch to vector store...")
                    try:
                        # Add texts using the collection directly with more error handling
                        for i, (text, meta) in enumerate(zip(batch_texts, batch_metas)):
                            logging.info(f"Adding chunk {i+1}/{len(batch_texts)}...")
                            try:
                                logging.info(f"Generating embedding for chunk {i+1}...")
                                embedding = embeddings.embed_query(text)
                                logging.info(f"Successfully generated embedding for chunk {i+1}")
                                
                                logging.info(f"Adding chunk {i+1} to collection...")
                                collection.add(
                                    embeddings=[embedding],
                                    documents=[text],
                                    metadatas=[meta],
                                    ids=[f"{doc['metadata']['source']}_{i}"]
                                )
                                logging.info(f"Successfully added chunk {i+1}")
                            except Exception as e:
                                logging.error(f"Error processing chunk {i+1}: {e}")
                                raise
                        logging.info("All chunks added to vector store.")
                        total_chunks += len(batch_texts)
                    except Exception as e:
                        logging.error(f"Error during vector store addition: {e}")
                        raise
                except Exception as e:
                    logging.error(f"Error during embedding or vector store addition: {e}")
                    raise
        except Exception as e:
            logging.error(f"Error adding batch to vector store: {e}")
        logging.info(f"Processed {len(batch_texts)} chunks from {doc['metadata']['source']}")

    logging.info(f"Processed {len(documents)} documents into {total_chunks} chunks")
    logging.info("Script finished execution.")

if __name__ == "__main__":
    main() 