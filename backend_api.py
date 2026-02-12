"""
FastAPI Backend for RAG System
Provides HTTP endpoints for the React frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import os
from pathlib import Path

from rag_system import RAGSystem

app = FastAPI(title="RAG System API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
rag = None
index_path = "rag_index"

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    retrieved_documents: List[Dict]

@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup"""
    global rag
    print("Initializing RAG System...")
    
    rag = RAGSystem(
        embedding_model_name="BAAI/bge-base-en-v1.5",
        chunk_size=512,
        chunk_overlap=50,
        top_k=3,
        groq_model="llama-3.1-8b-instant"
    )
    
    # Load existing index or create new one
    if os.path.exists(f"{index_path}.index"):
        print("Loading existing index...")
        rag.load_index(index_path)
    else:
        print("No index found. Please run main.py first to create the index.")
        # Create sample documents if needed
        documents_dir = Path("documents")
        if documents_dir.exists() and list(documents_dir.glob("*.txt")):
            print("Building index from documents...")
            document_paths = [str(p) for p in documents_dir.glob("*.txt")]
            documents = rag.load_documents(document_paths)
            rag.build_index(documents)
            rag.save_index(index_path)
    
    print("RAG System ready!")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "rag_initialized": rag is not None,
        "index_loaded": rag.index is not None if rag else False
    }

@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """Query the RAG system"""
    if not rag or not rag.index:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        result = rag.query(request.question)
        return QueryResponse(
            question=result['question'],
            answer=result['answer'],
            retrieved_documents=result['retrieved_documents']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/documents")
async def get_documents():
    """Get list of indexed documents"""
    if not rag:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    # Get unique sources from metadata
    sources = set()
    for doc in rag.metadata:
        sources.add(doc.get('source', 'unknown'))
    
    return {
        "total_chunks": len(rag.metadata),
        "sources": list(sources)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
