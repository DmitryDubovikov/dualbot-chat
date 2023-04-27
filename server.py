import socket
import threading
import logging

logging.basicConfig(
    filename="chat.log", format="%(asctime)s - %(message)s", level=logging.INFO
)

HOST = "127.0.0.1"
PORT = 12345

clients = []


def handle_messages(conn, addr):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode("utf-8")
            logging.info(f"Received from {addr[0]}:{addr[1]}: {message}")
            for client in clients:
                if client != conn:
                    client.sendall(data)
    except:
        logging.error(f"Connection with {addr[0]}:{addr[1]} lost unexpectedly")
    finally:
        if conn in clients:
            clients.remove(conn)
        conn.close()


def listen():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        logging.info(f"Server started on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            clients.append(conn)

            thread = threading.Thread(target=handle_messages, args=(conn, addr))
            thread.start()


listen()
