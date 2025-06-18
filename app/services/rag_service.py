from typing import List, Tuple
import requests
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma    import Chroma

from ..core.settings import get_settings
from ..core.roles    import get_allowed_departments
from ..schemas.chat  import ChatRequest, ChatResponse

settings = get_settings()

class RAGService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = Chroma(
            persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
            embedding_function=self.embeddings,
            collection_name="rbac"
        )

    def retrieve(self, query: str, role: str, k: int = 5) -> List[Tuple[str, dict]]:
        allowed = get_allowed_departments(role)
        hits = self.vector_store.similarity_search_with_score(query, k=k*3)
        filtered = []
        for doc, score in hits:
            department = doc.metadata.get("department", "general")
            if department in allowed:
                filtered.append((doc.page_content, doc.metadata))
                if len(filtered) >= k:
                    break
        return filtered

    def generate(self, query: str, context: List[str]) -> str:
        if not settings.GROQ_API_KEY or settings.GROQ_API_KEY == "your_groq_api_key_here":
            # Fallback response when Groq API key is not configured
            return f"I found some relevant information, but I need a Groq API key to generate a proper response. Here's what I found: {' '.join(context[:2])}"

        # Enhanced prompt template for better answer quality
        prompt = "\n".join([
            "You are a helpful assistant that answers questions based on the provided context information.",
            "Please provide clear, accurate, and well-structured answers.",
            "",
            "Context information:",
            "---------------------",
            *context,
            "---------------------",
            "",
            f"Question: {query}",
            "",
            "Instructions:",
            "- Answer based only on the context provided above",
            "- If the context doesn't contain enough information, say so clearly",
            "- Provide specific details and examples when available",
            "- Structure your answer in a clear, organized manner",
            "- Keep your answer concise but comprehensive",
            "",
            "Answer:"
        ])

        try:
            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",  # Fixed URL
                headers={
                    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": settings.GROQ_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,  # Reduced from 0.7 for more consistent answers
                    "max_tokens": 800,   # Increased from 500 for more detailed answers
                    "top_p": 0.9,
                    "frequency_penalty": 0.1,
                    "presence_penalty": 0.1
                },
                timeout=30  # Add timeout
            )
            
            if resp.status_code != 200:
                error_msg = f"Groq API error (Status {resp.status_code}): {resp.text}"
                print(f"Warning: {error_msg}")
                # Fallback to context summary
                return f"Based on the available information: {' '.join(context[:3])}"
                
            return resp.json()["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Request error: {str(e)}"
            print(f"Warning: {error_msg}")
            # Fallback to context summary
            return f"Based on the available information: {' '.join(context[:3])}"
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"Warning: {error_msg}")
            # Fallback to context summary
            return f"Based on the available information: {' '.join(context[:3])}"

    async def answer(self, req: ChatRequest, role: str) -> ChatResponse:
        docs = self.retrieve(req.message, role)
        if not docs:
            return ChatResponse(response="No relevant info found.", sources=[])
        context = [d[0] for d in docs]
        sources = [d[1]["source"] for d in docs]
        ans = self.generate(req.message, context)
        return ChatResponse(response=ans, sources=sources)

    def add_documents(self, documents: List[str]):
        # if you want dynamic uploads later
        texts = [d["content"] for d in documents]
        metas = [d["metadata"] for d in documents]
        self.vector_store.add_texts(texts=texts, metadatas=metas)
        self.vector_store.persist()
