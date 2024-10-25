import grpc
from concurrent import futures
from redis import Redis
from redisearch import Client, Query
import prize_pb2
import prize_pb2_grpc

# Create a connection to Redis using redis-py with username/password
redis_connection = Redis(
    host='redis-17148.c81.us-east-1-2.ec2.redns.redis-cloud.com',
    port=17148,
    username='admin',  # Provide the username here
    password='8Zm6U7UTiTzTMiw!',  # Provide the password here
    decode_responses=True  # To ensure the responses are properly decoded
)

# Now, create a RediSearch client using the Redis connection
redis_client = Client(
    'prizeIdx',  # The index you are querying
    conn=redis_connection  # Pass the Redis connection to RediSearch client
)

class NobelPrizeServiceServicer(prize_pb2_grpc.NobelPrizeServiceServicer):
    # The gRPC service implementation for each query
    
    def GetLaureatesByCategoryAndYearRange(self, request, context):
        # Query RediSearch based on the category and year range
        search_query = f"@category:{request.category} @year:[{request.start_year} {request.end_year}]"
        res = redis_client.search(Query(search_query))
        return prize_pb2.LaureatesResponse(total_laureates=res.total)

    def GetLaureatesByKeyword(self, request, context):
        # Query RediSearch based on a keyword in the motivation field
        search_query = f"@motivation:{request.keyword}"
        res = redis_client.search(Query(search_query))
        return prize_pb2.LaureatesResponse(total_laureates=res.total)

    def GetLaureateByName(self, request, context):
        # Query RediSearch for a laureate based on the first and last name
        search_query = f"@firstname:{request.first_name} @lastname:{request.last_name}"
        res = redis_client.search(Query(search_query))
        if res.total > 0:
            laureate = res.docs[0]
            return prize_pb2.LaureateDetailsResponse(
                year=laureate.year,
                category=laureate.category,
                motivation=laureate.motivation
            )
        return prize_pb2.LaureateDetailsResponse()

def serve():
    # Start the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    prize_pb2_grpc.add_NobelPrizeServiceServicer_to_server(NobelPrizeServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    if server.add_insecure_port('[::]:50051') != 0:
        print("gRPC server started on port 50051")
    else:
        print("Failed to start gRPC server.")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()