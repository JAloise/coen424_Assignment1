import time
import grpc
import prize_pb2
import prize_pb2_grpc
import matplotlib.pyplot as plt

#Store latency for 100
latencies = {"query1": [], "query2": [], "query3": []}

def measure_latency(stub, query_type, request): #calculates latency
    
    start_time = time.time() #timer stats, before sending request

    # Perform gRPC request based on query type
    if query_type == "query1":
        stub.GetLaureatesByCategoryAndYearRange(request)
    elif query_type == "query2":
        stub.GetLaureatesByKeyword(request)
    elif query_type == "query3":
        stub.GetLaureateByName(request)

    
    end_time = time.time() #Stores End time
    return end_time - start_time #Return the end-to-end delay (end - start)

def run_latency_tests():

    #Open gRPC channel and create stub
    with grpc.insecure_channel('localhost:50051') as channel:
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

def plot_latencies():
    #Box Plot for each query (milliseconds)
    plt.figure(figsize=(10, 6))

    #create box plots
    plt.boxplot([latency * 1000 for latency in latencies["query1"]],
                positions=[1], widths=0.4)  #Query1
    plt.boxplot([latency * 1000 for latency in latencies["query2"]],
                positions=[2], widths=0.4)  #Query2
    plt.boxplot([latency * 1000 for latency in latencies["query3"]],
                positions=[3], widths=0.4)  #Query3

    plt.xticks([1, 2, 3], ['Query1', 
                            'Query2', 
                            'Query3'])
    
    plt.ylabel('End-to-End Delay (ms)') #y-axis label
    plt.title('Box Plots of End-to-End Delays Per Query')#titles
    
    plt.ylim(15, 35)  # Adjust the y-axis scale

    plt.grid(axis='y')
    plt.show()

if __name__ == '__main__':
    run_latency_tests()
    plot_latencies()
