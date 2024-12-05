import asyncio
from client_api import ClientAPI

async def main():
    client = ClientAPI(('localhost', 8006))

    node_id = input("Enter the node ID to start e.g- 000,111,010. Only Enter node id which has failed!")
    if node_id == '000':
        port=8000
    elif node_id == '001':
        port=8001
    elif node_id == '010':
        port=8002
    elif node_id == '011':
        port=8003
    elif node_id == '100':
        port=8004
    elif node_id == '101':
        port=8005
    elif node_id == '110':
        port=8006
    elif node_id == '111':
        port=8007
        
    response = await client.start_new(node_id, port)
    print("START Node Response:", response)

# Run the publisher example
if __name__ == "__main__":
    asyncio.run(main())

