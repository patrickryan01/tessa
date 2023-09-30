import redis
from collections import Counter
import json

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)  # decode_responses will auto-decode UTF-8 for strings

def store_interaction(user_id, query, response):
    """
    Store the interaction in Redis.
    """
    data = {
        "query": query,
        "response": response
    }
    
    # Convert dict to a JSON string to store in Redis
    data_str = json.dumps(data)
    
    # Push the data to a list corresponding to the user
    r.lpush(f"user_data_{user_id}", data_str)

    # Limit list size to a maximum number (e.g., 1000) to save the last 1000 interactions
    r.ltrim(f"user_data_{user_id}", 0, 999)


def get_user_preference(user_id):
    """
    Retrieve and analyze user data to derive preferences based on frequency of queries.
    """
    user_data = r.lrange(f"user_data_{user_id}", 0, -1)  # Retrieve all stored interactions
    
    # Extract queries from data
    queries = [json.loads(data)["query"] for data in user_data]
    
    # Use Counter to find most common queries
    query_count = Counter(queries)
    frequently_asked = query_count.most_common(1)[0][0]
    
    return frequently_asked

# TODO: Implement reinforcement learning functions, feedback functions, etc.
# This would involve integrating libraries like TensorFlow or PyTorch, 
# defining the RL model, the reward system, training loop, etc.