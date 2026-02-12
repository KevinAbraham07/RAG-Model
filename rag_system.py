import os
from pymongo import MongoClient
from typing import List, Dict, Optional
from pathlib import Path
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class RAGSystem:

    def __init__(
        self,
        embedding_model_name: str = "BAAI/bge-base-en-v1.5",
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        top_k: int = 3,
        groq_api_key: Optional[str] = None,
        groq_model: str = "llama-3.1-8b-instant"
    ):

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k

        print(f"Loading embedding model: {embedding_model_name}...")
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
        print(f"Embedding dimension: {self.embedding_dim}")

        # MongoDB setup
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI not set in .env")

        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client["ragDB"]
        self.collection = self.db["documents"]

        print("MongoDB connected.")

        # Groq setup
        api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        if api_key:
            self.groq_client = Groq(api_key=api_key)
            self.groq_model = groq_model
            print("Groq client initialized.")
        else:
            self.groq_client = None
            print("Groq not configured.")

    def chunk_text(self, text: str) -> List[str]:
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk.strip())

            if end >= len(text):
                break

            start = end - self.chunk_overlap

        return chunks

    def load_documents(self, file_paths: List[str]) -> List[Dict]:
        all_chunks = []

        for file_path in file_paths:
            path = Path(file_path)
            if not path.exists():
                continue

            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            chunks = self.chunk_text(content)

            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    'text': chunk,
                    'source': str(path),
                    'chunk_id': i
                })

        return all_chunks

    def build_index(self, documents: List[Dict]):

        if not documents:
            raise ValueError("No documents provided")

        print("Storing embeddings in MongoDB...")

        for doc in documents:
            embedding = self.embedding_model.encode(doc['text']).tolist()

            self.collection.insert_one({
                "text": doc['text'],
                "source": doc['source'],
                "chunk_id": doc['chunk_id'],
                "embedding": embedding
            })

        print(f"Stored {len(documents)} documents.")

    def retrieve(self, query: str) -> List[Dict]:

        query_embedding = self.embedding_model.encode(query).tolist()

        results = self.collection.aggregate([
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": 100,
                    "limit": self.top_k
                }
            }
        ])

        retrieved_docs = []

        for doc in results:
            retrieved_docs.append({
                "text": doc["text"],
                "source": doc["source"],
                "score": doc.get("score", 0)
            })

        return retrieved_docs

    def generate_answer(self, query: str, context_docs: List[Dict]) -> str:

        if not self.groq_client:
            return "Groq not configured."

        context = "\n\n".join([
            f"[Source: {doc['source']}]\n{doc['text']}"
            for doc in context_docs
        ])

        prompt = f"""
Context:
{context}

Question:
{query}

Answer using only the context above.
"""

        response = self.groq_client.chat.completions.create(
            model=self.groq_model,
            messages=[
                {"role": "system", "content": "Answer based only on provided context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        return response.choices[0].message.content

    def query(self, question: str) -> Dict:

        retrieved_docs = self.retrieve(question)
        answer = self.generate_answer(question, retrieved_docs)

        return {
            "question": question,
            "retrieved_documents": retrieved_docs,
            "answer": answer
        }
