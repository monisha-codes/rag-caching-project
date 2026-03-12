# RAG Chatbot with Caching

This project implements a **Retrieval-Augmented Generation (RAG) Chatbot** with caching.  
The system retrieves relevant documents from a database and generates responses while using caching to improve response time.

---

## Technologies Used

- Python
- Django REST Framework
- PostgreSQL
- Redis
- Streamlit
- SentenceTransformers (for embeddings)

---

## Project Architecture

User Question  
↓  
Streamlit UI  
↓  
Django API  
↓  
Redis Cache  
↓  
Document Retrieval (PostgreSQL)  
↓  
Generate Answer  

---

## Features

- Retrieval-Augmented Generation (RAG)
- Redis key-value caching
- Semantic caching for similar questions
- Document retrieval using embeddings
- Query metrics tracking
- Simple Streamlit user interface

---

## Installation

### 1. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment (Windows):

```bash
venv\Scripts\activate
```

---

### 2. Install Dependencies

```bash
pip install django djangorestframework psycopg2-binary redis streamlit sentence-transformers numpy requests
```

---

### 3. Run Database Migrations

```bash
cd backend
python manage.py migrate
```

---

### 4. Load Documents

Open Django shell:

```bash
python manage.py shell
```

Run:

```python
from rag.ingestion import ingest_documents
ingest_documents("../data/documents.txt")
```

---

### 5. Run Backend

```bash
python manage.py runserver
```

Backend runs at:

```
http://localhost:8000
```

---

### 6. Run UI

```bash
streamlit run ui/app.py
```

Open:

```
http://localhost:8501
```

---

## Example

Ask a question:

```
How can I reset my password?
```

The system retrieves relevant documents and returns the answer.  
If the same question is asked again, the result is returned from cache with faster response time.