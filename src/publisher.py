# publisher_test.py
import asyncio
from client_api import ClientAPI

async def main():
    client = ClientAPI(('localhost', 8006))

    # Creating a publisher ID
    publisher_id = "publisher1"

    # Creating a publisher
    response = await client.create_publisher(publisher_id)
    print("Create Publisher Response:", response)

    # Creating a topic
    response = await client.create_topic(publisher_id, "news")
    print("Create Topic Response:", response)


    message = f"We have a new president"
    response = await client.publish_message(publisher_id, "news", message)
    print(f"Publish Message Response: {response} for message: {message}")
    
        # Deleting the topic
    #response = await client.delete_topic(publisher_id, "cricket")
    #print("Delete Topic Response:", response)
    
    #response = await client.stop_node(target_node='101')
    #print("STOP Node Response:", response)

# Run the publisher example
if __name__ == "__main__":
    asyncio.run(main())

