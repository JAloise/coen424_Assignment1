import redis
from redis.commands.search.query import Query
import json

#connect to redis
redis_client = redis.Redis(
    host = 'redis-17148.c81.us-east-1-2.ec2.redns.redis-cloud.com',
    port = 17148,
    password = '8Zm6U7UTiTzTMiw!',
    username = 'admin',
    decode_responses= True
)

# Query 2: Count laureates by motivation keyword
def count_laureates_by_motivation_keyword(keyword):
    query_string = f"@motivation:{keyword}"
    query = Query(query_string).return_fields('motivation').paging(0, 1000)
    
    # Execute the query using RedisSearch
    result = redis_client.ft('prizeIdx').search(query)
    
    # Calculate the total number of laureates
    total_laureates = len(result.docs)

    return total_laureates

# Main program to run the query
if __name__ == "__main__":
    print("Client Application for Nobel Prize Data Queries")

    # Prompt user for input
    keyword = input("Enter the keyword to search in motivation (e.g., democracy): ").strip()

    # Execute query
    total_laureates_by_keyword = count_laureates_by_motivation_keyword(keyword)

    # Display results
    print(f"Total laureates with motivation containing '{keyword}': {total_laureates_by_keyword}")