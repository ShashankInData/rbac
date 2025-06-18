# check_chroma.py
import chromadb
from app.core.settings import get_settings
import os

# Load your settings
settings = get_settings()
print(f"Chroma persist directory: {settings.CHROMA_PERSIST_DIRECTORY}")
print(f"Directory exists: {os.path.exists(settings.CHROMA_PERSIST_DIRECTORY)}")

# Initialize ChromaDB client directly
client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)

# Get or create collection
collection = client.get_or_create_collection(name="rbac")
print("\nCollection details:")
print(f"Name: {collection.name}")
print(f"Count: {collection.count()}")
print(f"Metadata: {collection.metadata}")

# Try to get some items
try:
    items = collection.get()
    print("\nItems in collection:")
    print(f"Number of items: {len(items['ids']) if items['ids'] else 0}")
except Exception as e:
    print(f"\nError getting items: {str(e)}")
