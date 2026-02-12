"""
Test script to check if all dependencies are properly installed
"""

print("Testing imports...")

try:
    import numpy as np
    print("[OK] numpy imported successfully")
except ImportError as e:
    print(f"[FAIL] numpy import failed: {e}")

try:
    import faiss
    print("[OK] faiss imported successfully")
except ImportError as e:
    print(f"[FAIL] faiss import failed: {e}")

try:
    from sentence_transformers import SentenceTransformer
    print("[OK] sentence_transformers imported successfully")
except ImportError as e:
    print(f"[FAIL] sentence_transformers import failed: {e}")

try:
    from groq import Groq
    print("[OK] groq imported successfully")
except ImportError as e:
    print(f"[FAIL] groq import failed: {e}")

try:
    from dotenv import load_dotenv
    print("[OK] python-dotenv imported successfully")
except ImportError as e:
    print(f"[FAIL] python-dotenv import failed: {e}")

try:
    from pathlib import Path
    print("[OK] pathlib imported successfully")
except ImportError as e:
    print(f"[FAIL] pathlib import failed: {e}")

try:
    from rag_system import RAGSystem
    print("[OK] rag_system imported successfully")
except ImportError as e:
    print(f"[FAIL] rag_system import failed: {e}")
except Exception as e:
    print(f"[FAIL] rag_system import error: {e}")

print("\nAll imports tested!")

