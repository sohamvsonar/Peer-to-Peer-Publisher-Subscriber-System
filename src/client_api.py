import asyncio
import json
from dht import hash_topic
from hypercube import Hypercube
from datetime import datetime

class ClientAPI:
    def __init__(self, peer_address):
        self.peer_address = peer_address
        self.host = '127.0.0.1'
        self.default_port = 8000
        self.log = []
        

    async def send_request(self, target_node, message):
        if target_node != 8000:
            self.hypercube = Hypercube(target_node)
            #print(self.hypercube.neighbors)
        if self.default_port == target_node:
            reader, writer = await asyncio.open_connection(self.host, self.default_port)
        else:
            try:
                target_port = self.default_port + int(target_node, 2)
                reader, writer = await asyncio.open_connection(self.host, target_port)
            except:
                print(f"Cannot connect to the original node as node has failed\nFound a replica on {self.hypercube.neighbors[0]} Forwading topic access to node {self.hypercube.neighbors[0]}")
                message_dict = json.loads(message)
                if message_dict["action"] == "subscribe":
                    message_dict["action"] = "replica_subscribe"
                    message = json.dumps(message_dict)
                    target_port = self.default_port + int(self.hypercube.neighbors[0], 2)
                    reader, writer = await asyncio.open_connection(self.host, target_port)
                else:
                    message_dict["action"] = "replica_pull"
                    message = json.dumps(message_dict)
                    #self.log_event(f"this is the")
                    target_port = self.default_port + int(self.hypercube.neighbors[0], 2)
                    reader, writer = await asyncio.open_connection(self.host, target_port)
     
        writer.write(message.encode())
        await writer.drain()
        response = await reader.read(4096)
        writer.close()
        return response.decode()
        
    async def send_request_stop(self, target_node, message):
        if self.default_port == target_node:
            reader, writer = await asyncio.open_connection(self.host, self.default_port)
        else:
            target_port = self.default_port + int(target_node, 2)
            reader, writer = await asyncio.open_connection(self.host, target_port)
        writer.write(message.encode())
        await writer.drain()
        response = await reader.read(4096)
        writer.close()
        return response.decode()

    async def send_request_start(self, target_node, message):
        if self.default_port == target_node:
            reader, writer = await asyncio.open_connection(self.host, self.default_port)
        else:
            target_port = self.default_port + int(target_node, 2)
            reader, writer = await asyncio.open_connection(self.host, target_port)
        writer.write(message.encode())
        await writer.drain()
        #response = await reader.read(4096)
        writer.close()
        return "Server started"

    async def create_publisher(self, publisher_id):
        target_node = 8000
        message = json.dumps({"action": "create_publisher", "publisher_id": publisher_id})
        return await self.send_request(target_node, message)

    async def create_subscriber(self, subscriber_id):
        target_node = 8000
        message = json.dumps({"action": "create_subscriber", "subscriber_id": subscriber_id})
        return await self.send_request(target_node, message)

    async def create_topic(self, publisher_id, topic_name):
        target_node = hash_topic(topic_name)
        message = json.dumps({"action": "create_topic", "publisher_id": publisher_id, "topic": topic_name})
        return await self.send_request(target_node, message)

    async def delete_topic(self, publisher_id, topic_name):
        target_node = hash_topic(topic_name)
        message = json.dumps({"action": "delete_topic", "publisher_id": publisher_id, "topic": topic_name})
        return await self.send_request(target_node, message)

    async def publish_message(self, publisher_id, topic_name, content):
        target_node = hash_topic(topic_name)
        message = json.dumps({"action": "publish", "publisher_id": publisher_id, "topic": topic_name, "content": content})
        return await self.send_request(target_node, message)

    async def subscribe(self, subscriber_id, topic_name):
        target_node = hash_topic(topic_name)
        message = json.dumps({"action": "subscribe", "subscriber_id": subscriber_id, "topic": topic_name})
        return await self.send_request(target_node, message)

    async def pull_message(self, subscriber_id, topic_name):
        target_node = hash_topic(topic_name)
        message = json.dumps({"action": "pull", "subscriber_id": subscriber_id, "topic": topic_name})
        return await self.send_request(target_node, message)
        
    async def stop_node(self, target_node, flag):
        message = json.dumps({"action": "stop_node", "flag": flag})
        return await self.send_request_stop(target_node, message)
        
    async def start_new(self, node_id, port):
        target_node=8000
        message = json.dumps({"action": "start_new", "node_id": node_id, "port": port})
        return await self.send_request_start(target_node, message)
                
    def log_event(self, message):
        timestamp = datetime.now().isoformat()
        self.log.append(f"[{timestamp}] {message}")
        print(self.log[-1])
        
            


