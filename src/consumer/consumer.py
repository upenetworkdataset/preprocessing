import socket
import time
from contextlib import closing

HOST = ""
PORT = 5000
LOGGER_HOST = "logger"
LOGGER_PORT = 6000
BUFFER_SIZE = 4096
RETRY_DELAY = 1.0
MAX_LOGGER_ATTEMPTS = 120


def _connect_logger() -> socket.socket:
    for attempt in range(1, MAX_LOGGER_ATTEMPTS + 1):
        try:
            return socket.create_connection((LOGGER_HOST, LOGGER_PORT))
        except OSError:
            time.sleep(RETRY_DELAY)
    raise RuntimeError("Unable to connect to logger after multiple attempts")


def _forward(conn: socket.socket, logger_sock: socket.socket) -> None:
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        logger_sock.sendall(data)


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print("Consumer listening...")

        while True:
            conn, addr = server.accept()
            print(f"Consumer connected by {addr}")
            with closing(conn):
                with _connect_logger() as logger_sock:
                    _forward(conn, logger_sock)


if __name__ == "__main__":
    main()
