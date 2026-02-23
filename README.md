# DocuMind AI

A production-ready, beginner-friendly Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF, DOCX, and TXT documents and query them using semantic search. This project is built completely from scratch using Python, without relying on high-level orchestration wrappers like LangChain, to demonstrate the core mechanics of vector embeddings and similarity search.

## Features

*   **Multi-Format Document Support**: Automatically extracts text from `.pdf` (using PyMuPDF), `.docx` (using python-docx), and standard `.txt` files.
*   **Semantic Text Chunking**: Splits large documents into manageable, overlapping chunks to preserve context and improve search accuracy.
*   **Local Vector Embeddings**: Uses HuggingFace's `sentence-transformers` (`all-MiniLM-L6-v2`) to generate dense vector embeddings locally without any API costs.
*   **High-Speed Vector Search**: Utilizes Meta's `FAISS` library for blazingly fast L2 distance similarity search in memory.
*   **Interactive UI**: Provides a clean, purely Python-based frontend using `Streamlit` complete with drag-and-drop file uploading and a chat interface.

## Tech Stack

*   **Frontend**: Streamlit
*   **Document Processing**: PyMuPDF (`fitz`), `python-docx`
*   **Machine Learning (Embeddings)**: `sentence-transformers`
*   **Vector Database**: `faiss-cpu`

## Installation

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.

### 2. Setup Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies.
```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

1. **Start the Application**: Run the Streamlit server from your terminal.
```bash
streamlit run app.py
```

2. **Upload Documents**: Open the provided local URL (usually `http://localhost:8501`) in your web browser. Use the sidebar to upload your PDF, DOCX, or TXT files.
3. **Process**: Click the "Process Documents" button to extract the text, generate embeddings, and store them in the FAISS index. Wait for the success message.
4. **Chat**: Use the chat input box at the bottom of the screen to ask questions. The chatbot will perform a semantic search against your uploaded files and return the most relevant context snippets.

## Project Structure

*   `app.py`: The main Streamlit application script containing the UI, upload logic, and chat loop.
*   `document_processor.py`: Contains the logic for reading text from different file types and the `chunk_text()` sliding-window function.
*   `vector_store.py`: Contains the `VectorStore` class which manages the SentenceTransformer model and the FAISS index memory state.
*   `requirements.txt`: The list of Python dependencies required to run the project.

