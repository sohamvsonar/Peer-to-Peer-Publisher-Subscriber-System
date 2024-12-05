import logging
from datetime import datetime



class Hypercube:
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = self.get_neighbors(node_id)
        self.log = []
   

    def get_neighbors(self, node_id):
        """Calculate the neighbors of a given node in a hypercube topology."""
        neighbors = []
        node_binary = int(node_id, 2)
        for i in range(len(node_id)):
            # Flip each bit to find neighbors
            neighbor = node_binary ^ (1 << i)
            neighbor_id = format(neighbor, '03b')
            neighbors.append(neighbor_id)
        return neighbors

    def get_routing_path(self, target_id):
        """Calculate routing path from current node to target node."""
        path = []
        current = int(self.node_id, 2)
        target = int(target_id, 2)
        while current != target:
            diff = current ^ target
            next_step = current ^ (1 << (diff.bit_length() - 1))
            path.append(format(next_step, '03b'))
            current = next_step
        logging.info(f"[{self.node_id}] Routing path to '{target_id}': {path}")
        return path
        
    def log_event(self, message):
        timestamp = datetime.now().isoformat()
        self.log.append(f"[{timestamp}] {message}")
        print(self.log[-1])

