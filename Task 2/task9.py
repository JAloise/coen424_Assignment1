import time
import grpc
import prize_pb2
import prize_pb2_grpc
import matplotlib.pyplot as plt

# To store latency data for 100 requests
latencies = {"query1": [], "query2": [], "query3": []}

def measure_latency(stub, query_type, request):
    # Start the timer right before sending the request
    start_time = time.time()

    # Perform the appropriate gRPC request based on query_type
    if query_type == "query1":
        stub.GetLaureatesByCategoryAndYearRange(request)
    elif query_type == "query2":
        stub.GetLaureatesByKeyword(request)
    elif query_type == "query3":
        stub.GetLaureateByName(request)

    # Record end time after response is received
    end_time = time.time()
    # Return the end-to-end delay
    return end_time - start_time

def run_latency_tests():
    # Open gRPC channel and create stub
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = prize_pb2_grpc.NobelPrizeServiceStub(channel)

        # Perform 100 latency measurements for each query type
        for _ in range(100):
            # Measure delay for Query 1: Category and Year Range
            latencies["query1"].append(measure_latency(
                stub, "query1", prize_pb2.CategoryYearRequest(category="physics", start_year=2013, end_year=2023)
            ))
            # Measure delay for Query 2: Keyword in motivation
            latencies["query2"].append(measure_latency(
                stub, "query2", prize_pb2.KeywordRequest(keyword="discovery")
            ))
            # Measure delay for Query 3: Laureate by Name
            latencies["query3"].append(measure_latency(
                stub, "query3", prize_pb2.NameRequest(first_name="Albert", last_name="Einstein")
            ))

def plot_latencies():
    # Create a box plot for each query's latencies in milliseconds
    plt.figure(figsize=(10, 6))

    # Create box plots for each query
    plt.boxplot([latency * 1000 for latency in latencies["query1"]],
                positions=[1], widths=0.4)  # Position 1
    plt.boxplot([latency * 1000 for latency in latencies["query2"]],
                positions=[2], widths=0.4)  # Position 2
    plt.boxplot([latency * 1000 for latency in latencies["query3"]],
                positions=[3], widths=0.4)  # Position 3

    plt.xticks([1, 2, 3], ['Query1', 
                            'Query2', 
                            'Query3'])
    
    plt.ylabel('End-to-End Delay (ms)')
    plt.title('Box Plots of End-to-End Delays Per Query')
    
    plt.ylim(15, 35)  # Adjust the y-axis scale

    plt.grid(axis='y')
    plt.show()

if __name__ == '__main__':
    run_latency_tests()
    plot_latencies()
