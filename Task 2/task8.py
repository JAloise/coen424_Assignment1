import time
import grpc
import prize_pb2
import prize_pb2_grpc

latencies = {"query1": [], "query2": [], "query3": []} #Store latency for 100


def measure_latency(stub, query_type, request): #calculates latency
    """Measure the latency of the specified gRPC request."""
    start_time = time.time() #timer stats, before sending request

    #Perform gRPC request based on query type
    if query_type == "query1":
        stub.GetLaureatesByCategoryAndYearRange(request)
    elif query_type == "query2":
        stub.GetLaureatesByKeyword(request)
    elif query_type == "query3":
        stub.GetLaureateByName(request)

    end_time = time.time()  #Stores End time
    return end_time - start_time #Return the end-to-end delay (end - start)

def run_latency_tests():
    """Run latency tests for each query type."""
    with grpc.insecure_channel('localhost:50051') as channel: #Open gRPC channel and create stub
        stub = prize_pb2_grpc.NobelPrizeServiceStub(channel)

        #Perform 100 measurements for each query type
        for _ in range(100):
            #Measure delay for Query1
            latencies["query1"].append(measure_latency(
                stub, "query1", prize_pb2.CategoryYearRequest(category="physics", start_year=2013, end_year=2023)
            ))
            #Measure delay for Query2
            latencies["query2"].append(measure_latency(
                stub, "query2", prize_pb2.KeywordRequest(keyword="discovery")
            ))
            #Measure delay for Query3
            latencies["query3"].append(measure_latency(
                stub, "query3", prize_pb2.NameRequest(first_name="Albert", last_name="Einstein")
            ))

def display_average_latencies():
    """Calculate and display the average latency for each query type in milliseconds."""
    for query, times in latencies.items():
        avg_latency_ms = (sum(times) / len(times)) * 1000  #Calculates Avg latency & convert to milliseconds
        print(f"{query} - Average latency: {avg_latency_ms:.2f} ms")

if __name__ == '__main__':
    run_latency_tests()
    display_average_latencies()
