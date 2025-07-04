import socket
import sys
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(msg)
        except:
            break

def start_client(ip, port, role, topic):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    # Send role and topic to server like: "PUBLISHER:TOPIC_A"
    sock.send(f"{role}:{topic}".encode())

    if role == "SUBSCRIBER":
        print(f"[Subscriber-{topic}] Connected to {ip}:{port}")
        threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()
        # Wait for input so the terminal doesn’t close
        input("[Press ENTER to exit subscriber]")
    elif role == "PUBLISHER":
        print(f"[Publisher-{topic}] Connected to {ip}:{port}")
        while True:
            msg = input(f"You ({topic}): ")
            sock.send(msg.encode())
            if msg.strip().lower() == "terminate":
                break

    sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python client.py <SERVER_IP> <PORT> <PUBLISHER/SUBSCRIBER> <TOPIC>")
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])
    role = sys.argv[3].upper()
    topic = sys.argv[4].upper()

    if role not in ["PUBLISHER", "SUBSCRIBER"]:
        print("Role must be PUBLISHER or SUBSCRIBER")
        sys.exit(1)

    start_client(ip, port, role, topic)

#python client.py 127.0.0.1 5000 SUBSCRIBER SPORTS
#python client.py 127.0.0.1 5000 SUBSCRIBER NEWS

#python client.py 127.0.0.1 5000 PUBLISHER SPORTS
#python client.py 127.0.0.1 5000 PUBLISHER NEWS
