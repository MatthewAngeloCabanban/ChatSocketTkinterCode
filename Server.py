import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 55555

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

# List to store connected clients
clients = []

# Broadcast messages to all connected clients
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                # Remove the broken connection
                clients.remove(client)

# Handle messages from clients
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                # Remove the disconnected client
                clients.remove(client_socket)
                break
            broadcast(message, client_socket)
        except:
            # Remove the disconnected client
            clients.remove(client_socket)
            break

# Accept and handle incoming connections
def accept_connections():
    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        print(f"Connection established with {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Start the server
print("Server is listening for connections...")
accept_connections()