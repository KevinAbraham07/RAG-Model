"""
Main script to demonstrate the MongoDB-based RAG system
"""

from rag_system import RAGSystem
from pathlib import Path


def main():
    print("=" * 60)
    print("Initializing RAG System (MongoDB Version)")
    print("=" * 60)

    # Initialize RAG system
    rag = RAGSystem(
        embedding_model_name="BAAI/bge-base-en-v1.5",
        chunk_size=512,
        chunk_overlap=50,
        top_k=3,
        groq_model="llama-3.1-8b-instant"
    )

    # Create example documents folder
    documents_dir = Path("documents")
    documents_dir.mkdir(exist_ok=True)

    # Sample agriculture documents
    sample_docs = {
        "crop_farming.txt": """
Crop farming is the practice of growing plants for food, fiber, and other agricultural products. 
Key factors include soil preparation, irrigation, fertilizer management, pest control, and proper harvesting.
        """,

        "livestock_management.txt": """
Livestock farming involves raising animals for meat, milk, eggs, and other products.
Important aspects include nutrition, breeding, disease prevention, and animal welfare.
        """,

        "sustainable_agriculture.txt": """
Sustainable agriculture focuses on environmental health, economic profitability, and social equity.
Practices include crop rotation, organic farming, water conservation, and renewable energy use.
        """
    }

    print("\nCreating sample documents...")
    for filename, content in sample_docs.items():
        filepath = documents_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"Created: {filename}")

    # Load documents
    print("\nLoading and indexing documents...")
    document_paths = [str(documents_dir / f) for f in sample_docs.keys()]
    documents = rag.load_documents(document_paths)

    # Store embeddings in MongoDB
    rag.build_index(documents)

    print("\n" + "=" * 60)
    print("RAG System Ready! Ask questions (type 'quit' to exit)")
    print("=" * 60)

    # Interactive Q&A loop
    while True:
        question = input("\nYour question: ").strip()

        if question.lower() in ["quit", "exit", "q"]:
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
