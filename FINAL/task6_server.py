import os
import grpc
from concurrent import futures
from redis import Redis
from redisearch import Client, Query
import prize_pb2
import prize_pb2_grpc
import json

# Connection
redis_connection = Redis(
    host='redis-17148.c81.us-east-1-2.ec2.redns.redis-cloud.com',
    port=17148,
    username='admin',
    password='8Zm6U7UTiTzTMiw!',
    decode_responses=True
)

# Create RediSearch client using redis connection
redis_client = Client(
    'prizeIdx',
    conn=redis_connection
)

class NobelPrizeServiceServicer(prize_pb2_grpc.NobelPrizeServiceServicer):
    
    def GetLaureatesByCategoryAndYearRange(self, request, context):
        search_query = f"@category:{request.category}"
        query = Query(search_query).return_fields('year', 'category').paging(0, 1000)
        res = redis_client.search(query)
        
        total_laureates = 0
        for doc in res.docs:
            doc_year = int(doc.year)
            if request.start_year <= doc_year <= request.end_year:
                total_laureates += 1
        
        # Return total
        return prize_pb2.LaureatesResponse(total_laureates=total_laureates)
    
    def GetLaureatesByKeyword(self, request, context):
        search_query = f"@motivation:{request.keyword}"
        res = redis_client.search(Query(search_query))
        return prize_pb2.LaureatesResponse(total_laureates=res.total)

    def GetLaureateByName(self, request, context):
        search_query = f"@firstname:{request.first_name} @surname:{request.last_name}"
        res = redis_client.search(Query(search_query).return_fields('year', 'category', 'motivation').paging(0, 1000))

        if res.total > 0:
            laureate = res.docs[0]
            return prize_pb2.LaureateDetailsResponse(
                year=laureate.year,
                category=laureate.category,
                motivation=laureate.motivation
            )
        return prize_pb2.LaureateDetailsResponse()


def serve():
    # Start server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    prize_pb2_grpc.add_NobelPrizeServiceServicer_to_server(NobelPrizeServiceServicer(), server)
    
    port = os.getenv('PORT', '50051')
    server.add_insecure_port(f'[::]:{port}')
    
    print(f'Server starting on port {port}...')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
