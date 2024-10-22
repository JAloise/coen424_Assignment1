import matplotlib.pyplot as plt

from task8 import latencies


# Plot the box plots for the latencies
def plot_latencies():
    plt.boxplot([latencies["query1"], latencies["query2"], latencies["query3"]], labels=["Query 1", "Query 2", "Query 3"])
    plt.ylabel('Latency (seconds)')
    plt.title('End-to-End Latency for 100 Runs per Query')
    plt.show()

if __name__ == '__main__':
    plot_latencies()
