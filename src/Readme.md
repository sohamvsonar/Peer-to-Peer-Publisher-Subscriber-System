- Name: Soham Sonar
- CWID: A20541266
- Section 01
- Project -
- Publisher/Subscriber-Peer to Peer System with Distributed hash Table
    • Replicated topics for performance optimization and fault tolerance.
    • Dynamic topology configuration (add & removal of Hypercube nodes).

# Peer-to-Peer Publisher-Subscriber System

Peer-to-Peer Publisher-Subscriber System with Enhanced Features
This project implements a Peer-to-Peer (P2P) publisher-subscriber system using Python. The system allows multiple peer nodes to publish messages to topics and subscribe to those topics to receive messages. The architecture has been enhanced to include replicated topics for performance optimization and fault tolerance, as well as dynamic topology configuration to support adding or removing nodes during runtime.

	

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Makefile Targets](#makefile-targets)
- [Testing](#testing)
- [Cleaning Up](#cleaning-up)
- [License](#license)

## Features

- **Multiple Peer Nodes**: Create and manage multiple peer nodes that can act as both publishers and subscribers.
- **Dynamic Topology**: Add and remove nodes during runtime while maintaining system consistency.
- **Replicated Topics**: Optimize performance by creating topic replicas and ensuring fault tolerance.
- **Topic Management**: Support for creating, deleting, and managing topics.
- **Message Publishing**: Ability to publish messages to topics.
- **Message Pulling**: Subscribers can pull messages from their subscribed topics.
- **Asynchronous Communication**: Utilizes asynchronous programming for efficient handling of concurrent requests.
- **Simple API**: Easy-to-use API for interacting with the publisher and subscriber functionalities.

## Technologies Used

- **Python 3.x**: The primary programming language used for development.
- **aiohttp**: For asynchronous HTTP communication.
- **asyncio**: For asynchronous programming.
- **pydantic**: For data validation and settings management.
- **pytest**: For testing the application.

## Requirements

Before you begin, ensure you have the following installed:

- **Python 3.7 or higher**
- **pip** (Python package installer)

### Install Dependencies

To install the required libraries, run:

```bash
make install
```

## Installation
1. Install dependencies
	make install
	
Alternatively, you can install dependencies manually:

```bash
pip install -r requirements.txt
```

2. Running All the 8 peer nodes in a hypercube together:

On a new terminal, run all peer nodes and active for all tests.

To start the all nodes:

```bash
make run_all_node
```

Alternatively, you can run the server manually:


python3 run_peers.py

Once the server is running, it will listen on localhost - 8000 to 8007 from node 000 to node 111 for incoming connections.

3. Running a single Peer node

Note:
First you have to terminate all peer nodes then only you will be able to start this one as both cannot run on same port!.

- To run the single peernode

```bash
make run_peernode
```

5. Running a Publisher

Remember all the peernodes should be running on a independent terminals. So first run make run_all_node then the following:
The publisher can register, create topics, and send messages. To run the publisher client:

```bash
make run_publisher
```

Alternatively, manually run the publisher:

python3 publisher.py

6. Running a Subscriber Client
Remember all the peernodes should be running on a independent terminals. So first run make run_all_node then the following:
The subscriber can register, subscribe to topics, and pull messages. To run the subscriber client:

```bash
make run_subscriber
```

Alternatively, manually run the subscriber:

python3 subscriber.py

7. Running Tests
To ensure the system is working correctly, you can run the test suite. This will check the functionality of all APIs like registering publishers, subscribers, creating topics, sending and pulling messages.

To run the tests:

```bash
make run_tests
```

Alternatively, run the tests manually:

python3 test_all_api.py
The tests will check each of the APIs and print the results, confirming whether the operations passed or failed.

8. Running API Benchmarks and Evaluations.
This project includes benchmark scripts to evaluate the system's performance under different loads. To run benchmarks for various API calls (e.g., createTopic, send, subscribe, pull), use the following command:

Now you can terminate the servers and peernodes in the main folder. Because for benchmarks the server and peernodes are modified.

Enter the tests folder and use the following commands - cd tests

(a) To run the benchmark -
	1. start all the peernodes - python3 run_peers.py
	Now on a new terminal - 
	2. Benchmark All APIs - python3 benchmark_all_api.py
	3. Fault Tolerance - python3 fault_tolerance.py
	

9. Cleaning Up
To remove any temporary files or caches:

```bash
make clean
```
# Dynamic Topology

1. Stopping a NOde

Note:Remember all the peernodes should be running on a independent terminals. So first run make run_all_node then the following:

- To stop a node

```bash
make stop_node
```

2. Starting a NOde

Note:Remember all the peernodes should be running on a independent terminals. So first run make run_all_node then the following:

- To start a node

```bash
make start_node
```

3. Test FAult Tolerance

Note:Remember all the peernodes should be running on a independent terminals. So first run make run_all_node then the following:

- To test

```bash
make test_failure
```
4. Test replica fetching

Note:Remember all the peernodes should be running on a independent terminals. So first run make run_all_node then the following:

- To test

```bash
make fetch_replica
```

This will remove compiled Python files and the __pycache__ directory.

# Directory Structure

├── client_api.py                # Client-side API for interacting with the Peernode and Indexing server
├── publisher.py                 # Sample publisher client implementation
├── subscriber.py                # Sample subscriber client implementation
├── test_all_api.py               # Test script to verify all API functionalities
├── peernode.py			#To run the peernode   (1,2,3)
|__ run_peers.py
├── requirements.txt             # List of Python dependencies
├── Makefile                     # Build and execution commands
└── README.md                    # Project documentation (this file)

# Conclusion
This enhanced P2P publisher-subscriber system now supports:

Dynamic node addition/removal.
Topic replication for fault tolerance and performance optimization.
The project demonstrates a robust and scalable architecture with APIs to register publishers/subscribers, create topics, send messages, subscribe to topics, and pull messages. The system also includes automated tests and benchmarks to evaluate performance under various conditions.

This README.md provides all the steps needed to understand, install, and run your publisher-subscriber system. It includes clear instructions on how to set up the environment, run tests, benchmark the system, and clean up files.
