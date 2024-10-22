import time
import grpc
import prize_pb2
import prize_pb2_grpc

# To store latency data for 100 requests
latencies = {"query1": [], "query2": [], "query3": []}

def measure_latency(stub, query_type, request):
    start_time = time.time()

    if query_type == "query1":
        stub.GetLaureatesByCategoryAndYearRange(request)
    elif query_type == "query2":
        stub.GetLaureatesByKeyword(request)
    elif query_type == "query3":
        stub.GetLaureateByName(request)

    end_time = time.time()
    return end_time - start_time

def run_latency_tests():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = prize_pb2_grpc.NobelPrizeServiceStub(channel)

        for _ in range(100):
            latencies["query1"].append(measure_latency(
                stub, "query1", prize_pb2.CategoryYearRequest(category="physics", start_year=2013, end_year=2023)
            ))
            latencies["query2"].append(measure_latency(
                stub, "query2", prize_pb2.KeywordRequest(keyword="discovery")
            ))
            latencies["query3"].append(measure_latency(
                stub, "query3", prize_pb2.NameRequest(first_name="Albert", last_name="Einstein")
            ))

if __name__ == '__main__':
    run_latency_tests()
