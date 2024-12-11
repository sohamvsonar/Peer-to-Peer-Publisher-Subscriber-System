# Peer-to-Peer-Publisher-Subscriber-System

This repository contains the implementation of a **peer-to-peer (P2P) topic-based publisher-subscriber system**. The system supports distributed messaging with fault tolerance, topic replication, and high performance. It uses a **hypercube topology** to connect peer nodes, ensuring efficient routing and scalability. The system is built using **Python** and leverages **asynchronous I/O (asyncio)** for handling concurrent operations.

---

## **Features**
1. **Topic-based Publish/Subscribe**:
   - Publishers can create topics and publish messages.
   - Subscribers can subscribe to topics and pull messages.

2. **Peer-to-Peer Architecture**:
   - Nodes act as peers and are responsible for storing topics and serving publish/subscribe requests.

3. **Fault Tolerance**:
   - Topics are replicated in neighboring nodes based on the hypercube topology.
   - In case of node failures, the replicas ensure data availability.

4. **Dynamic Topology**:
   - Nodes are connected in a hypercube structure, ensuring fast routing and scalability.

5. **Asynchronous Communication**:
   - Supports multiple concurrent requests using asyncio for non-blocking I/O.

6. **Logging and Monitoring**:
   - Logs all key operations such as node failures, topic replication, message publishing, and subscription activity.

7. **Performance Optimization**:
   - Load balancing for read-heavy workloads by leveraging topic replicas.
   - Efficient handling of node churn (join/leave events) without system downtime.

---

## **System Design**
### **1. Architecture**
- **Nodes**: Each peer node stores a portion of topics and acts as both a publisher and subscriber.
- **Hypercube Topology**:
  - Nodes are connected based on a hypercube structure, allowing efficient routing and fault tolerance.
  - For example, Node `[000]` connects to its neighbors `[001, 010, 100]`.

### **2. Fault Tolerance**
- Each topic is replicated in neighboring nodes.
- On node failure, neighboring nodes serve as backup to handle requests for replicated topics.

### **3. Supported APIs**
| API Name               | Parameters                      | Description                                                                 |
|------------------------|----------------------------------|-----------------------------------------------------------------------------|
| `create_publisher`     | `publisher_id`                  | Registers a new publisher in the system.                                   |
| `create_subscriber`    | `subscriber_id`                 | Registers a new subscriber in the system.                                  |
| `create_topic`         | `publisher_id, topic_name`      | Creates a new topic and replicates it to neighbors.                        |
| `delete_topic`         | `publisher_id, topic_name`      | Deletes a topic from the node and its replicas.                            |
| `publish_message`      | `publisher_id, topic_name, msg` | Publishes a message to the topic.                                          |
| `subscribe`            | `subscriber_id, topic_name`     | Subscribes to a topic and registers for updates.                           |
| `pull`                 | `subscriber_id, topic_name`     | Pulls messages from the topic.                                             |
| `stop_node`            | `node_id`                       | Simulates a node failure for testing fault tolerance.                      |

---

## Logging
- Logs all major actions, including:

- Topic creation and replication.
- Message publishing and subscription activity.
- Node failures and recoveries.
- Use logging module to view logs in the console or write them to a file.

## Benchmarks
- Fault Tolerance Performance
- Simulate node failures and measure response times for pull and publish_message APIs.
- Compare with the older system to verify performance improvements.

### Test Cases
| Scenario	                  | Description                                                                   |   
|-----------------------------|-------------------------------------------------------------------------------|
| Single Node Failure	Test    | response times for subscribers pulling data from replicas.                    |
| High Concurrency (N=4,8)	  | Measure throughput during concurrent requests with active topic replication.  |
| Dynamic Node Join/Leave	    | Add and remove nodes and validate consistent system behavior.                 |

## Future Enhancements
- Decentralized DHT-based routing for scalable topic lookups.
- Load balancing across multiple replicas for write-heavy workloads.
- Improved recovery mechanisms for dynamic topic redistribution.

## Contributing
- Contributions are welcome! Please submit issues or pull requests for bugs, enhancements, or feature requests.
