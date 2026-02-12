"""
Simple example demonstrating the RAG system usage
"""

from rag_system import RAGSystem
from pathlib import Path

def example():
    print("RAG System Example")
    print("=" * 50)
    
    # Initialize RAG system
    rag = RAGSystem(
        embedding_model_name="BAAI/bge-base-en-v1.5",
        chunk_size=256,
        chunk_overlap=25,
        top_k=2
    )
    
    # Create a sample document
    sample_text = """
    Machine Learning is a subset of artificial intelligence that focuses on 
    algorithms that can learn from data. It enables computers to learn and make 
    decisions without being explicitly programmed for every task.
    
    There are three main types of machine learning:
    1. Supervised Learning: Learning from labeled data
    2. Unsupervised Learning: Finding patterns in unlabeled data
    3. Reinforcement Learning: Learning through trial and error with rewards
    """
    
    # Save sample document
    doc_path = Path("sample_doc.txt")
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(sample_text)
    
    # Load and index document
    print("\nLoading document...")
    documents = rag.load_documents([str(doc_path)])
    print(f"Created {len(documents)} chunks")
    
    print("\nBuilding index...")
    rag.build_index(documents)
    
    # Test queries
    queries = [
        "What is machine learning?",
        "What are the types of machine learning?",
        "How does supervised learning work?"
    ]
    
    print("\n" + "=" * 50)
    print("Testing Queries")
    print("=" * 50)
    
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 50)
        
        # Retrieve documents
        retrieved = rag.retrieve(query)
        print(f"Retrieved {len(retrieved)} documents:")
        for i, doc in enumerate(retrieved, 1):
            print(f"  {i}. Score: {doc['score']:.4f}")
            print(f"     Text: {doc['text'][:100]}...")
        
        # Generate answer (if API key is available)
        if rag.groq_client:
            answer = rag.generate_answer(query, retrieved)
            print(f"\nAnswer: {answer}")
        else:
            print("\n(LLM generation skipped - no API key)")
    
    # Cleanup
    if doc_path.exists():
        doc_path.unlink()
    
    print("\n" + "=" * 50)
    print("Example completed!")

if __name__ == "__main__":
    example()

