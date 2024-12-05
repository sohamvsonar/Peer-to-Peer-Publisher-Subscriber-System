import asyncio
from client_api import ClientAPI

# Example usage
async def main():
    client = ClientAPI(('localhost', 8001))

    # Creating publisher and subscriber IDs
    publisher_id = "publisher1"
    subscriber_id = "subscriber1"

    # Creating a publisher
    response = await client.create_publisher(publisher_id)
    print("Create Publisher Response:", response)

    # Creating a subscriber
    response = await client.create_subscriber(subscriber_id)
    print("Create Subscriber Response:", response)

    # Creating a topic
    response = await client.create_topic(publisher_id, "news")
    print("Create Topic Response:", response)

    # Publishing a message
    response = await client.publish_message(publisher_id, "news", "New president has been elected")
    print("Publish Message Response:", response)

    # Subscribing to the topic
    response = await client.subscribe(subscriber_id, "news")
    print("Subscribe Response:", response)

    # Pulling messages from the topic
    response = await client.pull_message(subscriber_id, "news")
    print("Pull Message Response:", response)

    # Deleting the topic
    response = await client.delete_topic(publisher_id, "news")
    print("Delete Topic Response:", response)

# Run the example
asyncio.run(main())

