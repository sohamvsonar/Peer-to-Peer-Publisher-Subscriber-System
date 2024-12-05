import asyncio
from datetime import datetime
import hashlib
import json
import sys
from hypercube import Hypercube
from dht import hash_topic

class PeerNode:
    def __init__(self, node_id, port):
        self.node_id = node_id
        self.port = port
        self.topics = {}  # Locally hosted topics
        self.publishers = {}  # Stores publisher IDs
        self.subscribers = {}  # Stores subscriber IDs
        self.log = []
        self.dht = {}  # Distributed hash table mapping topic names to node IDs
        self.hypercube = Hypercube(node_id)
        self.replica_topics = {}
        self.log_event(f"[{self.node_id}] Neighbors: {self.hypercube.neighbors}")

    def log_event(self, message):
        timestamp = datetime.now().isoformat()
        self.log.append(f"[{timestamp}] {message}")
        print(self.log[-1])

    async def handle_client_request(self, reader, writer):
        data = await reader.read(1024)
        message = data.decode()
        message1 = data.decode().strip()
        command, *args = message1.split()
        self.log_event(f"Received message from client: {message}")

        try:
            request = json.loads(message)
            action = request.get("action")
            topic = request.get("topic")
            publisher_id = request.get("publisher_id")
            subscriber_id = request.get("subscriber_id")
            topic_name = request.get("topic_name")
            original_node = request.get("original_node")
            content = request.get("content")
            flag = request.get("flag")
            self.flag = flag
            node_id = request.get("node_id")
            port = request.get("port")
            #self.log_event(self.flag)

            if action == "create_replica":
                response = await self.create_replica(topic_name, original_node)
            elif action == "create_replica_message":
                response = await self.create_replica_message(topic_name, content)
            elif action == "delete_replica":
                response = await self.delete_replica(topic_name)
            elif action == "create_publisher":
                response = await self.create_publisher(publisher_id)
            elif action == "create_subscriber":
                response = await self.create_subscriber(subscriber_id)
            elif action == "create_topic":
                response = await self.create_topic(publisher_id, topic)
            elif action == "delete_topic":
                response = await self.delete_topic(publisher_id, topic)
            elif action == "publish":
                content = request.get("content")
                self.log_event(content)
                response = await self.publish_message(publisher_id, topic, content)
            elif action == "subscribe":
                response = await self.subscribe(subscriber_id, topic)
            elif action == "pull":
                response = await self.pull_message(subscriber_id, topic)
            elif action == "stop_node":
                response = await self.stop_node(flag)
            elif action == "replica_subscribe":
                response = await self.replica_subscribe(subscriber_id, topic)
            elif action == "replica_pull":
                response = await self.replica_pull(subscriber_id, topic)
            elif action == "start_new":
                self.log_event("Starting new node")
                response = await self.start_new(node_id, port)                            
            else:
                response = "Invalid action"

            self.log_event(f"Response to client: {response}")
            writer.write(response.encode())
        except json.JSONDecodeError:
            writer.write(b"Invalid JSON format.")
        await writer.drain()
        writer.close()
        
        
    async def create_replica_message(self, topic_name, content):
        """
        Save a replica of a topic on the current node in a separate dictionary.

        Args:
            topic_name (str): The name of the topic to replicate.
            original_node (str): The original node ID where the topic was created.
        """
        if topic_name in self.replica_topics:
            #self.log_event('checking request in replica message fun')
            self.replica_topics[topic_name]['message'] = content
            #self.log_event(self.replica_topics)
            return f"Replica message pushed into topic '{topic_name}' created in replica_topics."
        else:
            self.logger.warning(f"Replica of topic '{topic_name}' do not exists in replica_topics.")
            
    async def create_replica(self, topic_name, original_node):
        if topic_name not in self.replica_topics:
            #self.log_event('checking request in replica fun')
            self.replica_topics[topic_name] = {"original_node": original_node}
            #self.log_event(self.replica_topics)
            return f"Replica of topic '{topic_name}' created in replica_topics. Original node: {original_node}"
        else:
            self.log_event(f"Replica of topic '{topic_name}' already exists in replica_topics.")
            return f"Replica of topic '{topic_name}' already exists on this node {self.node_id}."

    async def delete_replica(self, topic_name):
        if topic_name in self.replica_topics:
            #self.log_event('checking request in replica fun')
            del self.replica_topics[topic_name]
            #self.log_event(self.replica_topics)
            return f"Replica of topic '{topic_name}' deleted in replica_topics."
        else:
            self.log_event(f"Replica of topic '{topic_name}' do not exist in replica_topics.")


    async def create_publisher(self, publisher_id):
        if publisher_id not in self.publishers:
            self.publishers[publisher_id] = []
            self.log_event(f"Publisher '{publisher_id}' created.")
            return f"Publisher ID '{publisher_id}' created."
        self.log_event(f"Publisher '{publisher_id}' already exists.")
        return f"Publisher ID '{publisher_id}' already exists."

    async def create_subscriber(self, subscriber_id):
        if subscriber_id not in self.subscribers:
            self.subscribers[subscriber_id] = []
            self.log_event(f"Subscriber '{subscriber_id}' created.")
            return f"Subscriber ID '{subscriber_id}' created."
        self.log_event(f"Subscriber '{subscriber_id}' already exists.")
        return f"Subscriber ID '{subscriber_id}' already exists."

    async def create_topic(self, publisher_id, topic_name):
        if self.node_id == node_id:
            self.topics[topic_name] = []
            self.dht[topic_name] = self.node_id
            self.log_event(f"Topic '{topic_name}' created locally on node '{self.node_id}'")
            for neighbor in self.hypercube.neighbors:
                try:
            # Calculate the neighbor's port number (assuming ports start at 8000)
                    port = 8000 + int(neighbor, 2)

            # Send a request to the neighbor to create a replica
                    #message = f"CREATE_REPLICA {topic_name} {self.node_id}"
                    message = json.dumps({"action": "create_replica", "topic_name": topic_name, "original_node": self.node_id})
                    response = await self.send_request_to_node(target_node=port, message=message)

                    if response:
                        self.log_event(f"{response}")
                    else:
                        self.log_event(f"Failed to create replica of topic '{topic_name}' on node {neighbor}. Response: {response}")

                except Exception as e:
                    self.log_event(f"Error while replicating topic '{topic_name}' to neighbor {neighbor}: {e}")
                    return f" Error creating Topic '{topic_name}' with publisher ID '{publisher_id}'."
            return f"Topic has been successfully created on {self.node_id} and all the replicas has been stored into neighbors {self.hypercube.neighbors}"
            
        else:
            self.log_event(f"Forwarding topic creation for '{topic_name}' to node '{node_id}'")
            response = await self.forward_request(node_id, {
                "action": "create_topic",
                "topic": topic_name,
                "publisher_id": publisher_id
            })
            return response  # Return the response received from the forward_request


    async def delete_topic(self, publisher_id, topic_name):
        self.log_event(f"Deleting topic '{topic_name}' with hashed node '{node_id}'")

        if self.node_id == node_id:
            if topic_name in self.topics:
                del self.topics[topic_name]
                del self.dht[topic_name]
                self.log_event(f"Topic '{topic_name}' deleted locally on node '{self.node_id}'")
                for neighbor in self.hypercube.neighbors:
                    try:
            # Calculate the neighbor's port number (assuming ports start at 8000)
                        port = 8000 + int(neighbor, 2)

            # Send a request to the neighbor to delete a replica
                        message = json.dumps({"action": "delete_replica", "topic_name": topic_name})
                        response = await self.send_request_to_node(target_node=port, message=message)

                        if response:
                            self.log_event(f"Replica of topic '{topic_name}' successfully deleted on node {neighbor}.")
                        else:
                            self.log_event(f"Failed to delete replica of topic '{topic_name}' on node {neighbor}. Response: {response}")

                    except Exception as e:
                        self.log_event(f"Error while deleting replicating topic '{topic_name}' from neighbor {neighbor}: {e}")
                        return f"Error deleting Topic '{topic_name}' with publisher ID '{publisher_id}'."
                return f"Topic has been successfully deleted on {self.node_id} and all the replicas has been deleted from the neighbors {self.hypercube.neighbors}"

            self.log_event(f"Topic '{topic_name}' not found on node '{self.node_id}'")
            return f"Topic '{topic_name}' not found."
        else:
            self.log_event(f"Forwarding topic deletion for '{topic_name}' to node '{node_id}'")
            response = await self.forward_request(node_id, {
                "action": "delete_topic",
                "topic": topic_name,
                "publisher_id": publisher_id
            })
            return response

    async def publish_message(self, publisher_id, topic_name, content):
        self.log_event(f"Publishing message to topic '{topic_name}' on node '{node_id}'")

        if self.node_id == node_id:
            if topic_name in self.topics:
                self.topics[topic_name].append(content)
                self.log_event(f"Message published to '{topic_name}' locally on node '{self.node_id}'")
                for neighbor in self.hypercube.neighbors:
                    try:
            # Calculate the neighbor's port number (assuming ports start at 8000)
                        port = 8000 + int(neighbor, 2)

            # Send a request to the neighbor to create a replica
                        message = json.dumps({"action": "create_replica_message", "topic_name": topic_name, "content": content})
                        response = await self.send_request_to_node(target_node=port, message=message)

                        if response:
                            self.log_event(f"Message published to'{topic_name}' successfully created on node {neighbor}.")
                        else:
                            self.log_event(f"Failed to push message into replica of topic '{topic_name}' on node {neighbor}. Response: {response}")
                    except Exception as e:
                        self.logger.error(f"Error while replicating topic '{topic_name}' to neighbor {neighbor}: {e}")
                        return f"Topic '{topic_name}' created with publisher ID '{publisher_id}'."

                return f"Message published to '{topic_name}' and the replicas {self.hypercube.neighbors}."
            self.log_event(f"Topic '{topic_name}' not found on node '{self.node_id}'")
            return f"Topic '{topic_name}' not found."
        else:
            self.log_event(f"Forwarding publish request for topic '{topic_name}' to node '{node_id}'")
            response = await self.forward_request(node_id, {
                "action": "publish_message",
                "topic": topic_name,
                "publisher_id": publisher_id,
                "content": content
            })
            return response

    async def pull_message(self, subscriber_id, topic_name):
        self.log_event(f"Pulling message from topic '{topic_name}' on node '{node_id}'")

        if self.node_id == node_id:
            if topic_name in self.topics:
                messages = self.topics[topic_name]
                self.log_event(f"Messages pulled from '{topic_name}' locally on node '{self.node_id}'")
                return json.dumps(messages)
            self.log_event(f"Topic '{topic_name}' not found on node '{self.node_id}'")
            return f"Topic '{topic_name}' not found."
        else:
            self.log_event(f"Forwarding pull request for topic '{topic_name}' to node '{node_id}'")
            response = await self.forward_request(node_id, {
                "action": "pull_message",
                "topic": topic_name,
                "suscriber_id": subscriber_id
            })
            return response

    async def replica_pull(self, subscriber_id, topic_name):
        self.log_event(f"Pulling message from topic '{topic_name}' on node '{node_id}'")
        if self.node_id == node_id:
            if topic_name in self.replica_topics:
                messages = self.replica_topics[topic_name]
                self.log_event(f"Messages pulled from '{topic_name}' locally on node '{self.node_id}'")
                return json.dumps(messages)
            self.log_event(f"Topic '{topic_name}' not found on node '{self.node_id}'")
            return f"Topic '{topic_name}' not found."
        else:
            self.log_event(f"Forwarding pull request for topic '{topic_name}' to node '{node_id}'")
            response = await self.forward_request(node_id, {
                "action": "pull_message",
                "topic": topic_name,
                "suscriber_id": subscriber_id
            })
            return response


    async def subscribe(self, subscriber_id, topic_name):
        self.log_event(self.topics)
        self.log_event(f"Subscriber '{subscriber_id}' attempting to subscribe to '{topic_name}'")
        if topic_name in self.topics:
            #self.subscribers[subscriber_id].append(topic_name)
            self.log_event(f"Subscriber '{subscriber_id}' subscribed to '{topic_name}'")
            return f"Subscriber ID '{subscriber_id}' subscribed to '{topic_name}'."
        self.log_event(f"Subscription failed for subscriber '{subscriber_id}' or topic '{topic_name}' not found")
        return f"Subscriber ID '{subscriber_id}' not found or topic '{topic_name}' not found."

    async def replica_subscribe(self, subscriber_id, topic_name):
        self.log_event(f"Subscriber '{subscriber_id}' attempting to subscribe to '{topic_name}'")
        if topic_name in self.replica_topics:
            #self.subscribers[subscriber_id].append(topic_name)
            self.log_event(f"Subscriber '{subscriber_id}' subscribed to '{topic_name}'")
            return f"Subscriber ID '{subscriber_id}' subscribed to '{topic_name}'."
        self.log_event(f"Subscription failed for subscriber '{subscriber_id}' or topic '{topic_name}' not found")
        return f"Subscriber ID '{subscriber_id}' not found or topic '{topic_name}' not found."
        
    async def start_server(self):
        self.server = await asyncio.start_server(self.handle_client_request, 'localhost', self.port)
        self.log_event(f"Server started on port {self.port}")
        try:
            async with self.server:
                try:
                    await self.server.serve_forever()
                except asyncio.CancelledError:
                    self.log_event(f"xxxxxxxxxxxxxx    Node {self.node_id} has been failed.   xxxxxxxxxxxxxxx")
                    if self.flag:
                        self.log_event(f"Node {self.node_id} is restarting after a failure.")
                        await asyncio.sleep(10)
                        # Restart the server
                        self.server = await asyncio.start_server(self.handle_client_request, 'localhost', self.port)
                        self.log_event(f"xxxxxxxxxxxxxx  Node {self.node_id} is back online in its original state. xxxxxxxxxxxxxxxx")
                        async with self.server:
                            await self.server.serve_forever()
                        #return f"Node {self.node_id} restarted after 15 seconds."


        except Exception as e:
            print(f"Server is not active")

    async def forward_request(self, node_id, message):
        path = self.hypercube.get_routing_path(node_id)
        if path:
            next_hop = path[0]
            port = 8000 + int(next_hop, 2)
            self.log_event(f"[{self.node_id}] Forwarding to {next_hop} at port {port}")

            try:
                reader, writer = await asyncio.open_connection("localhost", port)
                self.log_event(f"Sending message: {json.dumps(message)}")
                writer.write(json.dumps(message).encode())
                await writer.drain()

                response_data = await reader.read(1024)
                self.log_event(f"Received response: {response_data.decode()}")
                response = {'status': 'success', 'message': "Topic  created with publisher ID."}
                print(response)
                writer.close()
                await writer.wait_closed()
                return response
            except Exception as e:
                self.log_event(f"Error forwarding request: {e}")
                return {"status": "error", "message": str(e)}
        else:
            self.log_event(f"[{self.node_id}] No path to target {node_id}")
            return {"status": "No path to target"}

    async def send_request_to_node(self, target_node, message):
        reader, writer = await asyncio.open_connection('127.0.0.1', target_node)
        writer.write(message.encode())
        await writer.drain()
        response = await reader.read(4096)
        writer.close()
        return response.decode()

    async def stop_node(self, flag):
        """
        Stop the current node to simulate failure.
        """
        self.log_event(f"Node {self.node_id} is now simulating a failure.")
        self.server.close()  # Stop the asyncio server
        await self.server.wait_closed()  # Wait for it to fully close
        return f"Node has been failed"
        #self.log_event(f"Node sadad")
        #await asyncio.sleep(10)
        #self.log_event(f"Node {self.node_id} is restarting after a failure.")
    
    async def start_new(self, node_id, port):
        self.log_event("Inside start_new")
        #asyncio.run(main(node_id, port))
        node = PeerNode(node_id=node_id, port=int(port))
        await node.start_server()
    

async def main(node_id, port):
    try:
        node = PeerNode(node_id=node_id, port=int(port))
        await node.start_server()
    except Exception as e:
        print(f"Server is not active {e}")

if __name__ == "__main__":
    node_id = sys.argv[1]  # Get node_id from command-line argument
    port = sys.argv[2]     # Get port from command-line argument
    asyncio.run(main(node_id, port))

