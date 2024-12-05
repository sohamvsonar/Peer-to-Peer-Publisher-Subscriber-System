import time
import asyncio
from client_api import ClientAPI

async def experiment_fault_tolerance():
    client = ClientAPI(('localhost', 8001))
    
    # Create a publisher and a topic
    await client.create_publisher("pub1")
    await client.create_topic("pub1", "news")
    await client.publish_message("pub1", "news", "Important update")
    
    # Simulate a node failure
    await client.stop_node(target_node='100', flag = True)
    
    # Try to retrieve the message from other nodes
    for port in range(8002, 8005):
        client = ClientAPI(('localhost', port))
        response = await client.pull_message("sub1", "news")
        print(f"Node at port {port}: {response}")

asyncio.run(experiment_fault_tolerance())
