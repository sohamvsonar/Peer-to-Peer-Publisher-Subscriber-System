# subscriber_test.py
import asyncio
from client_api import ClientAPI

async def main():
    client = ClientAPI(('localhost', 8004))
    
    # Creating a subscriber ID
    subscriber_id = "subscribersa1"

    # Creating a subscriber
    #response = await client.create_subscriber(subscriber_id)
    #print("Create Subscriber Response:", response)

    # Subscribing to the topic
    response = await client.subscribe(subscriber_id, "news")
    print("Subscribe Response:", response)

    response = await client.pull_message(subscriber_id, "news")
    print("Pull Message Response:", response)

# Run the subscriber example
if __name__ == "__main__":
    asyncio.run(main())

