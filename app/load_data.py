import psycopg2
from embeddings import docs, embeddings

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="semanticdb",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

print("Inserting documents into database...")

for doc, emb in zip(docs, embeddings):

    cur.execute(
        """
        INSERT INTO documents (content, embedding)
        VALUES (%s, %s)
        """,
        (doc, emb.tolist())
    )

conn.commit()

print("Finished inserting data.")