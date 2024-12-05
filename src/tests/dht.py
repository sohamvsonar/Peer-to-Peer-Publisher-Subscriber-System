import hashlib
import logging

def hash_topic(topic_name):
    """Hash function to map a topic to a specific node in an 8-node network."""
    hashed_value = int(hashlib.sha256(topic_name.encode()).hexdigest(), 16)
    node_id = format(hashed_value % 8, '03b')  # Assuming 8 nodes (3-bit identifiers)
    return node_id  # Convert to 3-bit binary string

