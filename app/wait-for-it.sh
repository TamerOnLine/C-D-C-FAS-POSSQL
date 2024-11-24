import socket
import time
import sys

def wait_for_service(host, port, retries=10, delay=1):
    for _ in range(retries):
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"Service {host}:{port} is available!")
                return
        except (socket.timeout, ConnectionRefusedError):
            print(f"Waiting for {host}:{port}...")
            time.sleep(delay)
    print(f"Service {host}:{port} is not available after {retries} retries.")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: wait_for_it.py <host> <port> <command> [args...]")
        sys.exit(1)

    service_host = sys.argv[1]
    service_port = int(sys.argv[2])

    wait_for_service(service_host, service_port)

    # Run the provided command
    if len(sys.argv) > 3:
        command = sys.argv[3:]
        print(f"Running command: {' '.join(command)}")
        sys.exit(subprocess.run(command).returncode)
