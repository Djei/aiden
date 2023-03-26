import redis
from redis.commands.search.query import Query
from sentence_transformers import SentenceTransformer

# Connect to the Redis server
r = redis.Redis(host='localhost', port=6379, db=0)

# Load the pre-trained SBERT model
model = SentenceTransformer('paraphrase-distilroberta-base-v1')

# Input question
input_question = "What are the advantages of regular physical activity?"

# Generate the embedding for the input question
input_embedding = model.encode(input_question, convert_to_numpy=True).tobytes()

# Perform a vector similarity search in Redis
#prepare the query
q = Query(f'*=>[KNN 5 @embedding $vec_param AS vector_score]').sort_by('vector_score').paging(0, 1).return_fields('question', 'vector_score').dialect(2)
params_dict = {"vec_param": input_embedding}

#Execute the query
response = r.ft(index_name="questions").search(q, query_params = params_dict)

# Get the most similar question from the search result
print(response)
