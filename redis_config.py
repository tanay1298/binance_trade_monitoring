import redis

# Redis connection parameters
redis_host = 'localhost'
redis_port = 6379
redis_db = 0

# Create a Redis client object
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

# Test the connection
redis_client.set('test_key', 'test_value')
print(redis_client.get('test_key'))
