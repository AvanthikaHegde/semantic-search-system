from sklearn.datasets import fetch_20newsgroups
from sentence_transformers import SentenceTransformer

# Load dataset
data = fetch_20newsgroups(remove=('headers','footers','quotes'))
docs = data.data

print("Number of documents:", len(docs))

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
embeddings = model.encode(docs, show_progress_bar=True)

print("Embedding shape:", embeddings.shape)