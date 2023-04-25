import socket
from threading import Thread

HOST = "127.0.0.1"
PORT = 12345


def receive_messages(client_socket):
    while True:
        message = client_socket.recv(1024)
        print(f"Message received from the server: {message.decode()}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print(f"Connected to server {HOST}:{PORT}")

    Thread(target=receive_messages, args=(client_socket,)).start()

    while True:
        message = input("Enter your message: ")
        client_socket.sendall(message.encode())
