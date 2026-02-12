"""
RAG (Retrieval-Augmented Generation) System
A complete implementation of RAG using sentence-transformers, FAISS, and Groq LLM
"""

import os
import pickle
from typing import List, Dict, Optional
from pathlib import Path
import numpy as np

from sentence_transformers import SentenceTransformer
import faiss
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class RAGSystem:
    """
    A complete RAG system that combines document retrieval with LLM generation.
    """
    
    def __init__(
        self,
        embedding_model_name: str = "BAAI/bge-base-en-v1.5",
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        top_k: int = 3,
        groq_api_key: Optional[str] = None,
        groq_model: str = "llama-3.1-8b-instant"
    ):
        """
        Initialize the RAG system.
        
        Args:
            embedding_model_name: Name of the sentence transformer model
            chunk_size: Size of text chunks for splitting documents
            chunk_overlap: Overlap between chunks
            top_k: Number of top documents to retrieve
            groq_api_key: Groq API key (or set GROQ_API_KEY env var)
            groq_model: Groq model name to use
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        
        # Initialize embedding model
        print(f"Loading embedding model: {embedding_model_name}...")
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
        print(f"Embedding model loaded! Dimension: {self.embedding_dim}")
        
        # Initialize vector store
        self.index = None
        self.documents = []
        self.metadata = []
        
        # Initialize Groq client
        api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        if api_key:
            self.groq_client = Groq(api_key=api_key)
            self.groq_model = groq_model
            print(f"Groq client initialized with model: {groq_model}")
        else:
            self.groq_client = None
            print("Warning: Groq API key not found. Generation will be disabled.")
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of text chunks
        """
        # Simple chunking by character count with overlap
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
        """
        Load documents from files and chunk them.
        
        Args:
            file_paths: List of file paths to load
            
        Returns:
            List of document dictionaries with text and metadata
        """
        all_chunks = []
        
        for file_path in file_paths:
            path = Path(file_path)
            if not path.exists():
                print(f"Warning: File not found: {file_path}")
                continue
            
            # Read file content
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Chunk the document
            chunks = self.chunk_text(content)
            
            # Store chunks with metadata
            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    'text': chunk,
                    'source': str(path),
                    'chunk_id': i,
                    'total_chunks': len(chunks)
                })
            
            print(f"Loaded {len(chunks)} chunks from {path.name}")
        
        return all_chunks
    
    def build_index(self, documents: List[Dict]):
        """
        Build FAISS index from documents.
        
        Args:
            documents: List of document dictionaries
        """
        if not documents:
            raise ValueError("No documents provided")
        
        self.documents = documents
        
        # Extract texts
        texts = [doc['text'] for doc in documents]
        
        # Generate embeddings
        print("Generating embeddings...")
        embeddings = self.embedding_model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Create FAISS index
        self.index = faiss.IndexFlatIP(self.embedding_dim)  # Inner product for cosine similarity
        self.index.add(embeddings.astype('float32'))
        
        # Store metadata
        self.metadata = documents
        
        print(f"Index built with {len(documents)} documents")
    
    def retrieve(self, query: str) -> List[Dict]:
        """
        Retrieve top-k most relevant documents for a query.
        
        Args:
            query: Query string
            
        Returns:
            List of retrieved documents with scores
        """
        if self.index is None:
            raise ValueError("Index not built. Call build_index() first.")
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(
            [query],
            convert_to_numpy=True
        )
        
        # Normalize query embedding
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(
            query_embedding.astype('float32'),
            min(self.top_k, len(self.documents))
        )
        
        # Retrieve documents
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.metadata):
                doc = self.metadata[idx].copy()
                doc['score'] = float(score)
                results.append(doc)
        
        return results
    
    def generate_answer(self, query: str, context_docs: List[Dict]) -> str:
        """
        Generate answer using LLM with retrieved context.
        
        Args:
            query: User query
            context_docs: Retrieved context documents
            
        Returns:
            Generated answer
        """
        if not self.groq_client:
            return "LLM not available. Please set GROQ_API_KEY environment variable."
        
        # Prepare context
        context = "\n\n".join([
            f"[Document {i+1} from {doc.get('source', 'unknown')}]\n{doc['text']}"
            for i, doc in enumerate(context_docs)
        ])
        
        # Create prompt
        prompt = f"""You are a helpful assistant that answers questions based on the provided context.

Context:
{context}

Question: {query}

Please provide a comprehensive answer based on the context above. If the context doesn't contain enough information to answer the question, say so."""

        try:
            # Generate response
            response = self.groq_client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def query(self, question: str) -> Dict:
        """
        Complete RAG pipeline: retrieve and generate.
        
        Args:
            question: User question
            
        Returns:
            Dictionary with retrieved documents and generated answer
        """
        # Retrieve relevant documents
        retrieved_docs = self.retrieve(question)
        
        # Generate answer
        answer = self.generate_answer(question, retrieved_docs)
        
        return {
            'question': question,
            'retrieved_documents': retrieved_docs,
            'answer': answer
        }
    
    def save_index(self, filepath: str):
        """Save the FAISS index and metadata to disk."""
        if self.index is None:
            raise ValueError("No index to save")
        
        # Save FAISS index
        faiss.write_index(self.index, f"{filepath}.index")
        
        # Save metadata
        with open(f"{filepath}.metadata", 'wb') as f:
            pickle.dump({
                'documents': self.documents,
                'metadata': self.metadata,
                'chunk_size': self.chunk_size,
                'chunk_overlap': self.chunk_overlap,
                'top_k': self.top_k
            }, f)
        
        print(f"Index saved to {filepath}")
    
    def load_index(self, filepath: str):
        """Load the FAISS index and metadata from disk."""
        # Load FAISS index
        self.index = faiss.read_index(f"{filepath}.index")
        
        # Load metadata
        with open(f"{filepath}.metadata", 'rb') as f:
            data = pickle.load(f)
            self.documents = data['documents']
            self.metadata = data['metadata']
            self.chunk_size = data.get('chunk_size', self.chunk_size)
            self.chunk_overlap = data.get('chunk_overlap', self.chunk_overlap)
            self.top_k = data.get('top_k', self.top_k)
        
        print(f"Index loaded from {filepath}")

