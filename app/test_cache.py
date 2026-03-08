import psycopg2
import numpy as np
from sentence_transformers import SentenceTransformer
from cache import SemanticCache
from sklearn.metrics.pairwise import cosine_similarity

# connect to database
conn = psycopg2.connect(
    host="localhost",
    database="semanticdb",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# initialize cache
cache = SemanticCache()

# test query
query = "latest nasa mission"
print("\nQuery:", query)

# generate embedding
query_embedding = model.encode([query])[0]

# convert embedding to postgres vector format
query_vec = "[" + ",".join(map(str, query_embedding.tolist())) + "]"

# find nearest document using vector similarity search
cur.execute("""
SELECT id, content, embedding, dominant_cluster
FROM documents
ORDER BY embedding <-> %s
LIMIT 1
""", (query_vec,))

doc = cur.fetchone()

doc_id = doc[0]
doc_text = doc[1]
cluster = doc[3]

print("\nRetrieved document cluster:", cluster)

# convert stored vector string -> numpy array
emb_str = doc[2].strip("[]")
doc_embedding = np.array([float(x) for x in emb_str.split(",")])

# store in cache
cache.store(query, query_embedding, doc_text, cluster)

print("\nStored query in cache.")

# now try a similar query
new_query = "recent space exploration mission"
print("\nNew Query:", new_query)

new_embedding = model.encode([new_query])[0]

hit, entry, sim = cache.lookup(new_embedding, cluster)

print("\nCache hit:", hit)
print("Similarity:", sim)

if hit:
    print("\nCached result snippet:")
    print(entry["result"][:200])

print("\nCache stats:")
print(cache.stats())