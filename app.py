import streamlit as st
import tempfile
import os

from document_processor import extract_text, chunk_text
from vector_store import VectorStore

# Set page config
st.set_page_config(page_title="RAG Document Chatbot", page_icon="📄")

# Initialize session state for the vector store
if "vector_store" not in st.session_state:
    st.session_state.vector_store = VectorStore()
    
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title & intro
st.title("📄 RAG Document Chatbot")
st.markdown("Upload your PDF, DOCX, or TXT documents and explore them through semantic search.")

# Sidebar for document upload
with st.sidebar:
    st.header("Document Upload")
    uploaded_files = st.file_uploader(
        "Upload a document", 
        type=["pdf", "docx", "txt"], 
        accept_multiple_files=True
    )

    if st.button("Process Documents"):
        if not uploaded_files:
            st.warning("Please upload at least one document.")
        else:
            # Clear existing index before adding new documents
            st.session_state.vector_store.clear()
            
            total_chunks_added = 0
            
            with st.spinner("Extracting, chunking and embedding documents..."):
                for uploaded_file in uploaded_files:
                    # Save to a temporary file
                    temp_dir = tempfile.mkdtemp()
                    temp_path = os.path.join(temp_dir, uploaded_file.name)
                    
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Process file
                    extracted_text = extract_text(temp_path)
                    
                    if extracted_text.strip():
                        # Chunk the text
                        chunks = chunk_text(extracted_text, chunk_size=500, chunk_overlap=50)
                        
                        # Add to vector store
                        st.session_state.vector_store.add_chunks(chunks)
                        total_chunks_added += len(chunks)
                    else:
                        st.warning(f"No text could be extracted from {uploaded_file.name}")
                        
            st.success(f"Indexed {len(uploaded_files)} documents ({total_chunks_added} chunks) successfully!")

st.divider()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display semantic context if available for assistant messages
        if message["role"] == "assistant" and "context" in message:
            with st.expander("Show Retrieved Context"):
                for idx, c in enumerate(message["context"]):
                    st.markdown(f"**Chunk {idx+1} (Distance: {c['distance']:.4f}):**")
                    st.text(c['text'])

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Search the vector store for context
    with st.chat_message("assistant"):
        with st.spinner("Searching for context..."):
            results = st.session_state.vector_store.search(prompt, top_k=3)
            
            if not results:
                response = "I couldn't find any relevant context in the uploaded documents. Please ensure you have uploaded and processed documents."
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                # We can formulate an answer using the retrieved context directly.
                # Since we don't have LangChain/OpenAI attached to generate a dynamic text response,
                # we will just present the top chunk as the initial answer and list the context.
                
                # Combine top contexts into a single response
                response = f"Based on the semantic search, here is the most relevant snippet:\n\n> {results[0]['text'][:300]}..."
                
                st.markdown(response)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response,
                    "context": results
                })
