import time
import asyncio
from client_api import ClientAPI
import matplotlib.pyplot as plt

# Define constants for the benchmark
NUM_REQUESTS = 1000  # Number of requests per API
PEER_ADDRESS = "127.0.0.1"  # Assuming localhost for testing

async def benchmark_api(client, api_name, api_function, *args):
    latencies = []
    start_time = time.time()
    
    for _ in range(NUM_REQUESTS):
        req_start = time.time()
        await api_function(*args)
        latencies.append(time.time() - req_start)
    
    end_time = time.time()
    avg_latency = sum(latencies) / NUM_REQUESTS
    throughput = NUM_REQUESTS / (end_time - start_time)
    return avg_latency, throughput

async def run_benchmark():
    client = ClientAPI(PEER_ADDRESS)
    results = {}

    # Run benchmarks for each API
    results["create_publisher"] = await benchmark_api(client, "create_publisher", client.create_publisher, "pub1")
    results["create_subscriber"] = await benchmark_api(client, "create_subscriber", client.create_subscriber, "sub1")
    results["create_topic"] = await benchmark_api(client, "create_topic", client.create_topic, "pub1", "topic1")
    results["delete_topic"] = await benchmark_api(client, "delete_topic", client.delete_topic, "pub1", "topic1")
    results["publish_message"] = await benchmark_api(client, "publish_message", client.publish_message, "pub1", "topic1", "Hello")
    results["subscribe"] = await benchmark_api(client, "subscribe", client.subscribe, "sub1", "topic1")
    results["pull_message"] = await benchmark_api(client, "pull_message", client.pull_message, "sub1", "topic1")
    
    # Display results
    for api, (latency, throughput) in results.items():
        print(f"{api} - Avg Latency: {latency:.4f} seconds, Throughput: {throughput:.2f} requests/sec")
    
    return results

# Plot results
def plot_results(results):
    apis = list(results.keys())
    latencies = [results[api][0] for api in apis]
    throughputs = [results[api][1] for api in apis]

    fig, ax1 = plt.subplots()

    # Plot latency
    ax1.set_xlabel("API")
    ax1.set_ylabel("Avg Latency (s)", color="tab:blue")
    ax1.bar(apis, latencies, color="tab:blue", alpha=0.6)
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    # Plot throughput on the same graph with a secondary axis
    ax2 = ax1.twinx()
    ax2.set_ylabel("Throughput (requests/sec)", color="tab:red")
    ax2.plot(apis, throughputs, color="tab:red", marker="o", linestyle="--")
    ax2.tick_params(axis="y", labelcolor="tab:red")

    fig.tight_layout()
    plt.title("API Benchmark - Latency and Throughput")
    plt.show()

if __name__ == "__main__":
    results = asyncio.run(run_benchmark())
    plot_results(results)

