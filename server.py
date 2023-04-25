import socket
from threading import Thread

HOST = "127.0.0.1"
PORT = 12345


def handle_client(client_socket, client_address):
    print(f"Client connected {client_address}")

    while True:
        message = client_socket.recv(1024)
        if message:
            print(f"Message received from client {client_address}: {message.decode()}")
            broadcast(message, client_address)
        else:
            client_socket.close()
            break


def broadcast(message, sender_address):
    for client in clients:
        if client[1] != sender_address:
            client[0].sendall(message)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"The server is running on {HOST}:{PORT}")

    clients = []

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append((client_socket, client_address))
        Thread(target=handle_client, args=(client_socket, client_address)).start()
