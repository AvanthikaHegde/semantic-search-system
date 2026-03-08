

from pydantic import BaseModel
from fastapi import FastAPI
import psycopg2
import numpy as np
from sentence_transformers import SentenceTransformer
from app.cache import SemanticCache

class QueryRequest(BaseModel):
    query: str

app = FastAPI()

# load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# initialize semantic cache
cache = SemanticCache()

# connect to postgres
conn = psycopg2.connect(
    host="localhost",
    database="semanticdb",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()


@app.post("/query")
def query_api(request: QueryRequest):

    query = request.query

    # generate query embedding
    query_embedding = model.encode([query])[0]

    # convert to postgres vector format
    query_vec = "[" + ",".join(map(str, query_embedding.tolist())) + "]"

    # find most similar document
    cur.execute("""
    SELECT id, content, embedding, dominant_cluster
    FROM documents
    ORDER BY embedding <-> %s
    LIMIT 1
    """, (query_vec,))

    doc = cur.fetchone()

    doc_text = doc[1]
    cluster = doc[3]

    # check semantic cache
    hit, entry, sim = cache.lookup(query_embedding, cluster)

    if hit:

        return {
            "query": query,
            "cache_hit": True,
            "matched_query": entry["query"],
            "similarity_score": float(sim),
            "result": entry["result"],
            "dominant_cluster": entry["cluster"]
        }

    # cache miss → store result
    cache.store(query, query_embedding, doc_text, cluster)

    return {
        "query": query,
        "cache_hit": False,
        "matched_query": None,
        "similarity_score": float(sim),
        "result": doc_text,
        "dominant_cluster": cluster
    }


@app.get("/cache/stats")
def cache_stats():

    return cache.stats()


@app.delete("/cache")
def clear_cache():

    cache.clear()

    return {"message": "Cache cleared"}