"""
Non-interactive demo of the RAG system
"""

import sys
import os

# Fix Windows console encoding issues
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from rag_system import RAGSystem
from pathlib import Path

def demo():
    print("=" * 70)
    print("RAG SYSTEM DEMONSTRATION")
    print("=" * 70)
    
    # Initialize RAG system
    print("\n[1/5] Initializing RAG System...")
    print("-" * 70)
    rag = RAGSystem(
        embedding_model_name="BAAI/bge-base-en-v1.5",
        chunk_size=512,
        chunk_overlap=50,
        top_k=3,
        groq_model="llama-3.1-8b-instant"
    )
    
    # Check if index exists
    index_path = "rag_index"
    if os.path.exists(f"{index_path}.index"):
        print("\n[2/5] Loading existing vector index...")
        print("-" * 70)
        rag.load_index(index_path)
        print(f"Loaded index with {len(rag.documents)} document chunks")
    else:
        print("\n[2/5] Building vector index from documents...")
        print("-" * 70)
        
        # Create documents directory
        documents_dir = Path("documents")
        documents_dir.mkdir(exist_ok=True)
        
        # Sample documents - Agriculture focused
        sample_docs = {
            "crop_farming.txt": """
Crop farming is the practice of growing plants for food, fiber, and other agricultural products. 
The most common crops include grains like wheat, rice, and corn, as well as vegetables, fruits, 
and cash crops like cotton and coffee.

Successful crop farming requires understanding soil conditions, climate patterns, and proper 
irrigation techniques. Farmers must select appropriate crop varieties for their region and 
manage pests and diseases effectively.

Key factors in crop production include:
- Soil preparation and fertility management
- Seed selection and planting techniques
- Water management and irrigation systems
- Fertilizer application and nutrient management
- Pest and disease control
- Harvest timing and post-harvest handling

Modern agriculture also incorporates precision farming techniques using technology to optimize 
yields while minimizing environmental impact. Crop rotation and cover crops help maintain soil 
health and prevent erosion.
            """,
            
            "livestock_management.txt": """
Livestock farming involves raising animals for meat, milk, eggs, wool, and other products. 
Common livestock includes cattle, pigs, sheep, goats, chickens, and ducks.

Proper livestock management requires attention to animal health, nutrition, housing, and 
welfare. Farmers must provide adequate feed, clean water, shelter, and veterinary care.

Key aspects of livestock management include:
- Breeding and genetics for improved productivity
- Nutrition and feed management
- Disease prevention and veterinary care
- Housing and environmental conditions
- Animal welfare and ethical practices
- Waste management and environmental impact

Sustainable livestock farming focuses on efficient resource use, animal welfare, and 
minimizing environmental footprint. Pasture-based systems and rotational grazing can improve 
soil health while providing natural feed for animals.
            """,
            
            "sustainable_agriculture.txt": """
Sustainable agriculture is a farming approach that focuses on long-term environmental health, 
economic profitability, and social equity. It aims to meet current food needs without 
compromising the ability of future generations to meet their own needs.

Sustainable farming practices include:
- Organic farming methods that avoid synthetic pesticides and fertilizers
- Crop rotation and diversification to maintain soil health
- Integrated pest management (IPM) to reduce chemical use
- Water conservation and efficient irrigation systems
- Conservation tillage to reduce soil erosion
- Agroforestry combining trees with crops or livestock
- Renewable energy use on farms

Benefits of sustainable agriculture include:
- Improved soil health and fertility over time
- Reduced environmental pollution
- Enhanced biodiversity
- Better water quality and conservation
- Increased resilience to climate change
- Economic stability for farmers
- Healthier food products

Modern sustainable agriculture often combines traditional knowledge with innovative 
technologies like precision farming, renewable energy, and biological pest control methods.
            """
        }
        
        # Write documents
        for filename, content in sample_docs.items():
            filepath = documents_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content.strip())
        
        # Load and index
        document_paths = [str(documents_dir / f) for f in sample_docs.keys()]
        documents = rag.load_documents(document_paths)
        rag.build_index(documents)
        rag.save_index(index_path)
        print(f"Index built with {len(documents)} document chunks")
    
    # Test queries
    print("\n[3/5] Testing Document Retrieval...")
    print("-" * 70)
    
    test_queries = [
        "What is crop farming?",
        "What are the key aspects of livestock management?",
        "What is sustainable agriculture?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nQuery {i}: {query}")
        retrieved = rag.retrieve(query)
        print(f"  Retrieved {len(retrieved)} relevant chunks:")
        for j, doc in enumerate(retrieved, 1):
            print(f"    [{j}] Score: {doc['score']:.4f} | Source: {Path(doc['source']).name}")
            print(f"        Preview: {doc['text'][:80]}...")
    
    # Full RAG query
    print("\n[4/5] Full RAG Query (Retrieval + Generation)...")
    print("-" * 70)
    
    question = "What are the best practices for sustainable crop farming?"
    print(f"\nQuestion: {question}\n")
    
    result = rag.query(question)
    
    print("Retrieved Documents:")
    for i, doc in enumerate(result['retrieved_documents'], 1):
        print(f"\n  [{i}] Relevance Score: {doc['score']:.4f}")
        print(f"      Source: {Path(doc['source']).name}")
        print(f"      Content: {doc['text'][:150]}...")
    
    print("\n" + "-" * 70)
    print("Generated Answer:")
    print("-" * 70)
    print(result['answer'])
    
    # Explain the process
    print("\n[5/5] How RAG Works:")
    print("-" * 70)
    print("""
1. DOCUMENT PROCESSING:
   - Documents are split into overlapping chunks (512 chars with 50 char overlap)
   - Each chunk preserves context while keeping sizes manageable
   
2. EMBEDDING GENERATION:
   - Each chunk is converted to a 768-dimensional vector using BGE embedding model
   - Similar meanings produce similar vectors (semantic similarity)
   
3. VECTOR STORAGE:
   - Embeddings are stored in FAISS (Facebook AI Similarity Search) index
   - FAISS enables fast similarity search across millions of vectors
   
4. QUERY PROCESSING:
   - Your question is converted to the same vector space
   - FAISS finds the top-k most similar document chunks (cosine similarity)
   
5. ANSWER GENERATION:
   - Retrieved chunks provide context to the LLM
   - LLM generates an answer grounded in the retrieved facts
   - This reduces hallucinations and improves accuracy
   
BENEFITS:
- Answers are based on your specific documents
- Can handle questions beyond the LLM's training data
- Reduces false information (hallucinations)
- Easy to update by adding new documents
    """)
    
    print("=" * 70)
    print("Demo completed!")
    print("=" * 70)

if __name__ == "__main__":
    demo()

