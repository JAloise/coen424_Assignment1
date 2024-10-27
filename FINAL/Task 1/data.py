import redis
import requests
import json


#connect to redis
redis_client = redis.Redis(
    host = 'redis-17148.c81.us-east-1-2.ec2.redns.redis-cloud.com',
    port = 17148,
    password = '8Zm6U7UTiTzTMiw!',
    username = 'admin',
    decode_responses= True
)


# Function to fetch data from the Nobel Prize API
def fetch_nobel_prizes():
    url = "http://api.nobelprize.org/v1/prize.json"
    response = requests.get(url) #request fetches the content from url
    
    if response.status_code == 200:
        return response.json() #request returns response object
    else:
        print("Failed to fetch data from the API")
        return None
    

# Function to store data in Redis as JSON
def store_prizes_in_redis(prizes):
    for i, prize in enumerate(prizes['prizes']):
        key = f"prizes:{i+1}"  # Creating a unique key for each prize
        redis_client.json().set(key, '$', prize)  # Using Redis JSON command to store
       

# Main logic
def main():
    
    prizes = fetch_nobel_prizes() #Fetch and Store JSON object in 'prizes' variable
    
    if prizes: #prizes contains JSON object then executes
        store_prizes_in_redis(prizes)
        print("All data stored successfully!")
    else:
        print("No data to store.")

if __name__ == "__main__":
    main()