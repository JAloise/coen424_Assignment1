import time
import grpc
import prize_pb2
import prize_pb2_grpc

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
    latency = end_time - start_time
    return latency

def run_latency_tests():
    cloud_run_url = "grpc-server-751936615562.us-central1.run.app"

    credentials = grpc.ssl_channel_credentials()

    with grpc.secure_channel(f'{cloud_run_url}:443', credentials) as channel:
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

        print(f"Query 1 Average Latency: {sum(latencies['query1']) / len(latencies['query1']) * 1000:.2f} ms")
        print(f"Query 2 Average Latency: {sum(latencies['query2']) / len(latencies['query2']) * 1000:.2f} ms")
        print(f"Query 3 Average Latency: {sum(latencies['query3']) / len(latencies['query3']) * 1000:.2f} ms")

if __name__ == '__main__':
    run_latency_tests()
