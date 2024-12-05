import asyncio
import os

# Define node IDs and corresponding ports
nodes = [
    ("000", 8000),
    ("001", 8001),
    ("010", 8002),
    ("011", 8003),
    ("100", 8004),
    ("101", 8005),
    ("110", 8006),
    ("111", 8007)
]

async def start_peer_node(node_id, port):
    """Start a PeerNode process with unbuffered output."""
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"  # Ensure no buffering in subprocess

    process = await asyncio.create_subprocess_exec(
        "python", "peernode.py", node_id, str(port),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env  # Pass the modified environment
    )
    print(f"Started node {node_id} on port {port}")

    # Read and print output from stdout and stderr continuously
    async def read_stream(stream, name):
        while True:
            line = await stream.readline()
            if line:
                print(f"[{name}] {line.decode().strip()}", flush=True)
            else:
                break

    # Run both stdout and stderr readers
    await asyncio.gather(
        read_stream(process.stdout, f"Node {node_id}"),
        read_stream(process.stderr, f"Node {node_id} Error")
    )

async def main():
    # Start all nodes as concurrent tasks
    tasks = [start_peer_node(node_id, port) for node_id, port in nodes]
    await asyncio.gather(*tasks)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nShutting down nodes...")

