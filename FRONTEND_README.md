# RAG System Frontend

## ✅ System Status

Your RAG system is now fully operational with a beautiful web interface!

## 🚀 Quick Start

### Backend (Already Running)
The FastAPI backend is running on **http://localhost:8000**

### Frontend
Open the frontend in your browser:
- **File**: `c:\Users\kevin\RAG\frontend.html`
- Just double-click the file or it should already be open in your browser!

## 📋 Features

### Chat Interface
- **Modern UI**: Dark theme with gradient accents
- **Real-time Q&A**: Ask questions about your documents
- **Loading Indicators**: Visual feedback while processing
- **Message History**: See all your previous questions and answers

### Source Panel
- **Retrieved Documents**: View the top 3 most relevant document chunks
- **Relevance Scores**: See how well each source matches your query
- **Source Metadata**: File names, chunk numbers, and full text preview
- **Toggle View**: Show/hide sources with a single click

## 🎨 Design

The interface features:
- **Gradient backgrounds**: Slate-900 to Slate-800
- **Glassmorphism effects**: Backdrop blur and transparency
- **Smooth animations**: Transitions and loading indicators
- **Responsive layout**: Adapts to different screen sizes
- **Custom scrollbars**: Styled to match the dark theme

## 🔧 Technical Stack

### Backend
- **FastAPI**: Modern Python web framework
- **RAG System**: Your existing `rag_system.py`
- **CORS Enabled**: Allows frontend to communicate with backend
- **Endpoints**:
  - `POST /query`: Submit questions
  - `GET /health`: Check system status
  - `GET /documents`: List indexed documents

### Frontend
- **Pure HTML/CSS/JavaScript**: No build step required
- **Tailwind CSS**: Via CDN for styling
- **Fetch API**: For backend communication
- **Vanilla JS**: No framework dependencies

## 📝 How It Works

1. **User asks a question** in the chat interface
2. **Frontend sends** the question to `http://localhost:8000/query`
3. **Backend processes**:
   - Embeds the question using `BAAI/bge-base-en-v1.5`
   - Searches FAISS index for top 3 relevant chunks
   - Sends chunks + question to Groq's Llama 3.1
   - Returns generated answer + source documents
4. **Frontend displays**:
   - The AI-generated answer
   - Retrieved source documents with scores
   - Metadata about each source

## 🎯 Example Questions

Try asking:
- "What is sustainable agriculture?"
- "Tell me about crop farming techniques"
- "How do I manage livestock?"
- "What are the benefits of organic farming?"

## 🛠️ Troubleshooting

### Backend Not Responding
If you get connection errors:
```bash
# Restart the backend
cd c:\Users\kevin\RAG
venv\Scripts\python.exe backend_api.py
```

### No Documents Found
If the system says no index exists:
```bash
# Run the main script to create the index
cd c:\Users\kevin\RAG
venv\Scripts\python.exe main.py
```

## 📂 File Structure

```
RAG/
├── backend_api.py          # FastAPI server
├── rag_system.py           # Core RAG logic
├── frontend.html           # Web interface (standalone)
├── documents/              # Your knowledge base
│   ├── crop_farming.txt
│   ├── livestock_management.txt
│   └── sustainable_agriculture.txt
├── rag_index.index         # FAISS vector index
└── rag_index.metadata      # Document metadata
```

## 🎉 Success!

Your RAG system is now accessible through a beautiful, modern web interface that replicates the functionality of `main.py` but with a much better user experience!

Enjoy chatting with your documents! 🚀
