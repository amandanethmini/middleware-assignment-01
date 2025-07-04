import socket
import sys

def start_client(server_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    print(f"[Client] Connected to {server_ip}:{port}")

    while True:
        message = input("[Client] Enter message: ")
        client_socket.sendall(message.encode())
        if message.strip().lower() == "terminate":
            print("[Client] Terminating connection.")
            break

    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <SERVER_IP> <PORT>")
        sys.exit(1)
    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    start_client(server_ip, port)

#python client.py 127.0.0.1 5000