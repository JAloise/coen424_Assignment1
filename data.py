import redis
import requests
import json


#connect to redis
redis_client = redis.Redis(
    host = 'redis-14661.c16.us-east-1-2.ec2.redns.redis-cloud.com',
    port = 14661,
    password = 'fgDlVtbeMimm3Ueao5jiGlZqtIlBoxsv',
    decode_responses= True
)


# Function to fetch data from the Nobel Prize API
def fetch_nobel_prizes():
    url = "http://api.nobelprize.org/v1/prize.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data from the API")
        return None
    
# Function to store data in Redis as JSON
def store_prizes_in_redis(prizes):
    for i, prize in enumerate(prizes['prizes']):
        key = f"prizes:{i+1}"  # Creating a unique key for each prize
        redis_client.json().set(key, '$', json.dumps(prize))  # Using Redis JSON command to store
        
        print(f"Stored {key} in Redis")

# Main logic
def main():
    # Fetch the Nobel Prize data
    prizes = fetch_nobel_prizes()
    
    if prizes:
        # Store the data in Redis
        store_prizes_in_redis(prizes)
        print("All data stored successfully!")
    else:
        print("No data to store.")

if __name__ == "__main__":
    main()