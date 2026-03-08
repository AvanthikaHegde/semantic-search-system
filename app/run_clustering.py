import psycopg2
import numpy as np
import skfuzzy as fuzz

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="semanticdb",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

print("Loading embeddings from database...")

# Get embeddings
cur.execute("SELECT id, embedding FROM documents")

rows = cur.fetchall()

doc_ids = []
embeddings = []

for row in rows:
    doc_ids.append(row[0])

    # convert postgres vector string → list of floats
    emb_str = row[1].strip("[]")
    emb = np.array([float(x) for x in emb_str.split(",")])

    embeddings.append(emb)
    
embeddings = np.array(embeddings)

print("Total documents:", len(embeddings))


# Run fuzzy clustering
clusters = 15

print("Running fuzzy clustering...")

cntr, u, _, _, _, _, _ = fuzz.cluster.cmeans(
    embeddings.T,
    c=clusters,
    m=2,
    error=0.005,
    maxiter=1000
)

# u = membership matrix
# shape = clusters x documents

dominant_clusters = np.argmax(u, axis=0)

print("Updating database with cluster assignments...")

for doc_id, cluster in zip(doc_ids, dominant_clusters):

    cur.execute(
        """
        UPDATE documents
        SET dominant_cluster = %s
        WHERE id = %s
        """,
        (int(cluster), doc_id)
    )

conn.commit()

print("Clustering complete.")