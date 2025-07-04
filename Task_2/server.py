import socket
import threading
import sys

subscribers = []  # List to store subscriber sockets
lock = threading.Lock()

def handle_client(client_socket, address, role):
    print(f"[Server] {role} connected from {address}")

    try:
        while True:
            message = client_socket.recv(1024).decode().strip()
            if not message or message.lower() == "terminate":
                print(f"[Server] {role} at {address} disconnected.")
                break

            if role == "PUBLISHER":
                with lock:
                    for subscriber_socket in subscribers:
                        try:
                            subscriber_socket.sendall(f"[Publisher @ {address}]: {message}\n".encode())
                        except:
                            continue  # Ignore broken pipe errors
    except Exception as e:
        print(f"[Server] Error with {role} @ {address}: {e}")
    finally:
        client_socket.close()
        if role == "SUBSCRIBER":
            with lock:
                if client_socket in subscribers:
                    subscribers.remove(client_socket)

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen()
    print(f"[Server] Listening on port {port}...")

    while True:
        client_socket, addr = server_socket.accept()
        role = client_socket.recv(1024).decode().strip().upper()
        if role == "SUBSCRIBER":
            with lock:
                subscribers.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, role))
        client_thread.start()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
        sys.exit(1)
    port = int(sys.argv[1])
    start_server(port)

#python server.py 5000