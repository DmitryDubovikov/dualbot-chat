import socket
import sys
import threading


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "127.0.0.1"
PORT = 12345
nickname = ""

client_socket.connect((HOST, PORT))
print(f"[CONNECTED] Connected to {HOST}:{PORT}")


def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except socket.error as e:
            print(f"[ERROR] Socket error occurred: {str(e)}")
            sys.exit()


def send_messages():
    while True:
        try:
            message = input()
            if message.lower() == "quit":
                break
            message = f"{nickname} says: " + message
            client_socket.send(message.encode())
        except socket.error as e:
            print(f"[ERROR] Socket error occurred: {str(e)}")
            sys.exit()


nickname = input("Enter your nickname: ")


receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)
receive_thread.start()
send_thread.start()


receive_thread.join()
send_thread.join()


client_socket.close()
print("[DISCONNECTED] Client disconnected.")
