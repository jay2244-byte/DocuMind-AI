import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """Initializes the Sentence Transformer model and FAISS index."""
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        # embedding dimension for 'all-MiniLM-L6-v2' is 384
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        # Initialize an empty L2 distance FAISS index
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # We need to map FAISS internal IDs to our actual text chunks
        self.chunks_mapping = []

    def add_chunks(self, chunks):
        """Generates embeddings for a list of text chunks and adds them to the FAISS index."""
        if not chunks:
            return
            
        print(f"Embedding {len(chunks)} chunks...")
        # Encode chunks into dense vectors
        embeddings = self.model.encode(chunks, convert_to_numpy=True)
        
        # FAISS expects float32
        faiss.normalize_L2(embeddings) # Optional, usually good for cosine similarity if using IP, but we're using L2. Normalizing for better bounds.
        embeddings = np.array(embeddings, dtype='float32')
        
        # Add to FAISS index
        self.index.add(embeddings)
        
        # Update mapping
        self.chunks_mapping.extend(chunks)

    def search(self, query, top_k=3):
        """Embeds a query, searches the index, and returns the top-k most relevant chunks."""
        if self.index.ntotal == 0:
            return []
            
        print(f"Searching for query: '{query}'")
        # Encode query
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        query_embedding = np.array(query_embedding, dtype='float32')
        
        # Perform search using L2 distance
        # D is standard distance array, I is index array
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        # Return chunks corresponding to matched indices
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.chunks_mapping):
                # Optionally filter by distance if needed, here we just return all
                results.append({
                    "text": self.chunks_mapping[idx],
                    "distance": float(distances[0][i])
                })
                
        return results

    def clear(self):
        """Clears the FAISS index and chunk mapping."""
        self.index.reset()
        self.chunks_mapping = []
