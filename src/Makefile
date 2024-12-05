# Target to install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Target to run all the 8 peer nodes
run_all_node:
	@echo "Starting All the 8 Peer Nodes..."
	python3 run_peers.py

# Target to run the Peer Node 1
run_peernode:
	@echo "Running Peer Node 1..."
	python3 peernode.py 000 8000
	
# Target to run a publisher
run_publisher:
	@echo "Running publisher client..."
	python3 publisher.py

# Target to run a subscriber
run_subscriber:
	@echo "Running subscriber client..."
	python3 subscriber.py

# Target to run the tests
run_tests:
	@echo "Running all the API test cases"
	python3 test_all_api.py
	
# Target to stop the Node
stop_node:
	@echo "Stopping the node"
	python3 stop_node.py

# Target to start the Node
start_node:
	@echo "Starting the node"
	python3 start_node.py
	
# Target to run the failure tolerance tests
test_failure:
	@echo "Testing failure tolerance"
	python3 test_failure.py

# Target to run the repllica tests
fetch_replica:
	@echo "Testing the fetch_replica"
	python3 fetch_replica.py

# Target to clean up
clean:
	@echo "Cleaning up..."
	rm -rf *.pyc __pycache__
