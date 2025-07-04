import socket
import sys
import threading

def receive_messages(client_socket):
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(data.strip())
    except:
        pass

def start_client(server_ip, port, role):
    role = role.upper()
    if role not in ["PUBLISHER", "SUBSCRIBER"]:
        print("Invalid role. Use PUBLISHER or SUBSCRIBER.")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    # Send role to server
    client_socket.sendall(role.encode())

    print(f"[Client] Connected as {role} to {server_ip}:{port}")

    if role == "SUBSCRIBER":
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True
        receive_thread.start()

    try:
        while True:
            if role == "PUBLISHER":
                message = input("[Publisher] Enter message: ")
                client_socket.sendall(message.encode())
                if message.strip().lower() == "terminate":
                    break
            elif role == "SUBSCRIBER":
                # Just keep running; messages come from server
                pass
    except KeyboardInterrupt:
        pass
    finally:
        client_socket.close()
        print("[Client] Disconnected.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <SERVER_IP> <PORT> <ROLE>")
        sys.exit(1)
    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    role = sys.argv[3]
    start_client(server_ip, port, role)

#python client.py 127.0.0.1 5000 PUBLISHER
#python client.py 127.0.0.1 5000 SUBSCRIBER
