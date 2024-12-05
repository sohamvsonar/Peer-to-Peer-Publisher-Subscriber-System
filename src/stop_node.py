# publisher_test.py
import asyncio
from client_api import ClientAPI

async def main():
    client = ClientAPI(('localhost', 8006))

    target_node = input("Enter the node id which you want to stop e.g - 000, 010,111")
    response = await client.stop_node(target_node, flag = False)
    print("STOP Node Response:", response)

# Run the publisher example
if __name__ == "__main__":
    asyncio.run(main())

