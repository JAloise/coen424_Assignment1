import redis
from redis.commands.search.query import Query

#connect to redis
redis_client = redis.Redis(
    host = 'redis-17148.c81.us-east-1-2.ec2.redns.redis-cloud.com',
    port = 17148,
    password = '8Zm6U7UTiTzTMiw!',
    username = 'admin',
    decode_responses= True
)

# Query 3
def get_laureate_details(first_name, last_name):
    # Query by first name and last name
    query_string = f"@firstname:{first_name} @surname:{last_name}"
    query = Query(query_string).return_fields('year', 'category', 'motivation').paging(0, 1000)

    # Execute query using RedisSearch
    result = redis_client.ft('prizeIdx').search(query)

    laureate_details = []
    for doc in result.docs:
        details = {
            "year": doc.year,
            "category": doc.category,
            "motivation": doc.motivation
        }
        laureate_details.append(details)
    
    return laureate_details

if __name__ == "__main__":
    first_name = input("Enter the first name of the laureate: ").strip()
    last_name = input("Enter the last name of the laureate: ").strip()

    # Execute query
    laureate_info = get_laureate_details(first_name, last_name)

    # Display results
    if laureate_info:
        for info in laureate_info:
            print(f"Year: {info['year']}, Category: {info['category']}, Motivation: {info['motivation']}")
    else:
        print(f"No laureate found with name {first_name} {last_name}.")