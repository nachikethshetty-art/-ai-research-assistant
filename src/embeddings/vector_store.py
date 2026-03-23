import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = faiss.IndexFlatL2(384)  # 384 is the embedding size for MiniLM

    def add_texts(self, texts):
        """Generate embeddings for texts and add them to the FAISS index."""
        embeddings = self.model.encode(texts)
        self.index.add(np.array(embeddings, dtype='float32'))

    def search(self, query, top_k=5):
        """Search for the top_k most similar texts to the query."""
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding, dtype='float32'), top_k)
        return distances, indices

# Example usage
if __name__ == "__main__":
    store = VectorStore()
    texts = [
        "Lithium-ion batteries are widely used.",
        "Recycling technologies are advancing rapidly.",
        "Sustainability is a key focus in battery research."
    ]
    store.add_texts(texts)

    query = "What are the advancements in battery recycling?"
    distances, indices = store.search(query)
    print("Distances:", distances)
    print("Indices:", indices)