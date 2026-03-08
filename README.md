Semantic Search System with Intelligent Cache

**1.Overview:**

This project implements a semantic search system for the 20 Newsgroups dataset. Instead of relying on keyword matching, the system retrieves documents based on the meaning of a query.
To improve efficiency, the system includes a semantic cache that detects when two queries are similar and reuses previously computed results instead of performing the search again.
The system is exposed through a FastAPI service, allowing users to interact with it through a simple API.

System Workflow:


<img width="430" height="722" alt="image" src="https://github.com/user-attachments/assets/e7366b94-b6dd-4101-b2ff-bf8771196444" />





**2.Tech Stack:**

The project combines several tools to build the semantic search pipeline.

*Python
 Main programming language used for data processing, clustering, caching logic, and the API service.

*Sentence Transformers
 The model all-MiniLM-L6-v2 is used to convert text into 384-dimensional embeddings.
 These embeddings capture the semantic meaning of documents and queries.

*PostgreSQL & pgvector
 PostgreSQL is used as the database, while the pgvector extension enables efficient similarity search between vector embeddings.

*Fuzzy Clustering
 The Fuzzy C-Means clustering is applied to the document embeddings.Since documents can belong to multiple topics, fuzzy clustering helps represent overlapping semantic structures.

*FastAPI
 FastAPI exposes the system as a REST API, allowing users to submit queries and retrieve results easily.

*Docker
 Docker is used to run the PostgreSQL database with pgvector, ensuring the project can be reproduced easily.




**3.Why This System Is Efficient:**

This project improves search efficiency using several design choices:

Semantic Search:
Documents are retrieved using vector similarity, allowing the system to understand the meaning of queries instead of relying on exact word matches.

Semantic Cache:
Previously answered queries are stored along with their embeddings.
If a new query is similar enough to a cached query, the system reuses the cached result, avoiding unnecessary database searches.

Cluster-Aware Cache Lookup:
To reduce computation, cache lookup is restricted to queries belonging to the same semantic cluster.
This significantly reduces the number of comparisons needed as the cache grows.

Similarity Threshold:
A configurable similarity threshold determines whether two queries are close enough to reuse cached results, balancing accuracy and efficiency.




**4.Dataset:**

The system uses the 20 Newsgroups dataset, which contains posts from 20 different discussion topics.
The dataset was loaded using: __fetch_20newsgroups__

Key preprocessing steps:

-Removed email headers

-Removed footers

-Removed quoted replies

This ensures the embeddings capture the actual content of the document.

For this project a total of documents used were 11,314 covering 20 topics.


**5.API Endpoints**

The FastAPI service provides three endpoints.

_POST /query_

Submit a natural language query.

Example request:

<img width="324" height="109" alt="image" src="https://github.com/user-attachments/assets/c3a42ef4-5c6e-4c83-997e-768c8dc260d6" />


Example response:

<img width="299" height="206" alt="image" src="https://github.com/user-attachments/assets/b9cd5209-f1f0-4650-855c-5d9ae216eade" />



_GET /cache/stats_

Returns statistics about the cache.
Example:

<img width="291" height="222" alt="image" src="https://github.com/user-attachments/assets/50d3728a-b7bd-4c71-8ea2-feac97329427" />


_DELETE /cache_

Clears the semantic cache and resets statistics.


**6.Running the Project**
1. Install dependencies
   
        pip install -r requirements.txt
   
2. Start the PostgreSQL database
   
        docker compose up -d
   
3. Start the FastAPI server
   
       uvicorn app.main:app --reload
   
5. Open the API interface
   
       http://localhost:8000/docs

FastAPI provides an interactive interface where you can test the endpoints.

Overall Directory Structure:

<img width="369" height="348" alt="image" src="https://github.com/user-attachments/assets/efbc01e9-1d26-4955-9610-db771bd97055" />





