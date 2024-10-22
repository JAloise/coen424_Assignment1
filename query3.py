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

# Query 3: Get laureate details by first name and last name
def get_laureate_details(first_name, last_name):
    # Query by first name and last name
    query_string = f"@firstname:{first_name} @surname:{last_name}"
    query = Query(query_string).return_fields('year', 'category', 'motivation').paging(0, 1000)

    # Execute the query using RedisSearch
    result = redis_client.ft('prizeIdx').search(query)

    # Extract and return year, category, and motivation
    laureate_details = []
    for doc in result.docs:
        details = {
            "year": doc.year,  # Access year directly from the Document object
            "category": doc.category,  # Access category directly from the Document object
            "motivation": doc.motivation  # Access motivation directly
        }
        laureate_details.append(details)
    
    return laureate_details

# Main program to run the query
if __name__ == "__main__":
    print("Client Application for Nobel Prize Data Queries")

    # Prompt user for input
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