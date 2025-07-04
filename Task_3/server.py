import socket
import threading
import sys
from collections import defaultdict

# Dictionary to hold subscribers per topic
topics = defaultdict(list)
lock = threading.Lock()

def handle_client(client_socket, addr):
    try:
        # Receive role and topic in format: "ROLE:TOPIC"
        data = client_socket.recv(1024).decode()
        role, topic = data.strip().upper().split(":", 1)

        print(f"[Server] {role} connected from {addr} on topic '{topic}'")

        if role == "SUBSCRIBER":
            with lock:
                topics[topic].append(client_socket)

        while True:
            message = client_socket.recv(1024).decode()
            if not message or message.strip().lower() == "terminate":
                print(f"[Server] {role} at {addr} disconnected.")
                break

            if role == "PUBLISHER":
                print(f"[Publisher @ {addr} - {topic}]: {message}")
                with lock:
                    for sub in topics[topic]:
                        try:
                            sub.send(f"[{topic}] {message}".encode())
                        except:
                            topics[topic].remove(sub)

    except Exception as e:
        print(f"[Server] Error: {e}")
    finally:
        client_socket.close()
        if role == "SUBSCRIBER":
            with lock:
                if client_socket in topics[topic]:
                    topics[topic].remove(client_socket)

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(10)
    print(f"[Server] Listening on port {port}...")

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)

#python server.py 5000
