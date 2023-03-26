This is a small mock project playing with SBERT to create embeddings for questions and store them in redis

### Pre-requisites
- Python3.10

### Setup
- `source venv/bin/activate`
- `pip install`

### How to run?
- `docker compose up`

#### Create embeddings
- `python demo/store_questions_embeddings.py`

#### Query embeddings
- `python demo/query_questions_embeddings.py`