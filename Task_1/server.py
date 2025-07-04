import socket
import sys

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"[Server] Listening on port {port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[Server] Connected to {addr}")
        while True:
            data = client_socket.recv(1024).decode()
            if not data or data.strip().lower() == "terminate":
                print(f"[Server] Client at {addr} disconnected.")
                break
            print(f"[Client @ {addr}] {data}")
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
        sys.exit(1)
    port = int(sys.argv[1])
    start_server(port)

#python server.py 5000