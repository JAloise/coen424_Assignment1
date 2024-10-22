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

# count laureates by category and year range
def count_laureates_by_category_and_year_range(category, start_year, end_year):
    # query by category and year range
    total_laureates = 0
    for year in range(start_year, end_year + 1):
        query_string = f"@category:{category} @year:{year}"
        query = Query(query_string).return_fields('year', 'category').paging(0, 1000)
        
        # Execute query using RedisSearch
        result = redis_client.ft('prizeIdx').search(query)
        
        # Count number of documents returned
        total_laureates += len(result.docs)

    return total_laureates

if __name__ == "__main__":
    print("Client Application for Nobel Prize Data Queries")

    # user input
    category = input("Enter the Nobel Prize category (e.g. peace): ").strip()
    start_year = int(input("Enter start year (min 2013): ").strip())
    end_year = int(input("Enter end year (max 2023): ").strip())

    # function call
    total_laureates = count_laureates_by_category_and_year_range(category, start_year, end_year)
    
    # Display
    print(f"Total laureates in category '{category}' between {start_year} and {end_year}: {total_laureates}")