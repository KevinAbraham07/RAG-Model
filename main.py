"""
Main script to demonstrate the RAG system
"""

from rag_system import RAGSystem
from pathlib import Path
import os

def main():
    # Initialize RAG system
    print("=" * 60)
    print("Initializing RAG System")
    print("=" * 60)
    
    rag = RAGSystem(
        embedding_model_name="BAAI/bge-base-en-v1.5",
        chunk_size=512,
        chunk_overlap=50,
        top_k=3,
        groq_model="llama-3.1-8b-instant"
    )
    
    # Check if index already exists
    index_path = "rag_index"
    if os.path.exists(f"{index_path}.index"):
        print("\nLoading existing index...")
        rag.load_index(index_path)
    else:
        # Create example documents if they don't exist
        documents_dir = Path("documents")
        documents_dir.mkdir(exist_ok=True)
        
        # Create sample documents - Agriculture focused
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
        
        # Write sample documents
        print("\nCreating sample documents...")
        for filename, content in sample_docs.items():
            filepath = documents_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content.strip())
            print(f"Created: {filename}")
        
        # Load documents and build index
        print("\nBuilding vector index...")
        document_paths = [str(documents_dir / f) for f in sample_docs.keys()]
        documents = rag.load_documents(document_paths)
        rag.build_index(documents)
        
        # Save index for future use
        rag.save_index(index_path)
    
    # Interactive Q&A
    print("\n" + "=" * 60)
    print("RAG System Ready! Ask questions (type 'quit' to exit)")
    print("=" * 60)
    
    while True:
        question = input("\nYour question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not question:
            continue
        
        print("\nProcessing your question...")
        result = rag.query(question)
        
        print("\n" + "-" * 60)
        print("RETRIEVED DOCUMENTS:")
        print("-" * 60)
        for i, doc in enumerate(result['retrieved_documents'], 1):
            print(f"\n[{i}] Score: {doc['score']:.4f}")
            print(f"Source: {doc['source']}")
            print(f"Text: {doc['text'][:200]}...")
        
        print("\n" + "-" * 60)
        print("GENERATED ANSWER:")
        print("-" * 60)
        print(result['answer'])
        print()

if __name__ == "__main__":
    main()
