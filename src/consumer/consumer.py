import socket
import json
import time

HOST = ""
PORT = 5000

LOGGER_HOST = "logger"
LOGGER_PORT = 6000


def connect_to_logger():
    """Establish connection to logger service"""
    while True:
        try:
            logger_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            logger_sock.connect((LOGGER_HOST, LOGGER_PORT))
            print(f"Connected to logger at {LOGGER_HOST}:{LOGGER_PORT}")
            return logger_sock
        except (socket.error, ConnectionRefusedError) as e:
            print(f"Cannot connect to logger: {e}. Retrying in 5 seconds...")
            time.sleep(5)


def forward_to_logger(logger_sock, event_data):
    """Forward event data to logger for storage"""
    try:
        logger_sock.sendall((event_data + "\n").encode())
        return True
    except (socket.error, BrokenPipeError) as e:
        print(f"Error forwarding to logger: {e}")
        return False


def process_malware_event(event_data, logger_sock):
    """Process and display malware event data"""
    try:
        event = json.loads(event_data)
        malware_type = event.get("malware_type", "unknown")
        timestamp = event.get("timestamp", 0)
        src_ip = event.get("source_ip", "N/A")
        dest_ip = event.get("dest_ip", "N/A")

        print(f"[{malware_type}] {src_ip} -> {dest_ip} @ {timestamp}")

        # Forward to logger for storage
        forward_to_logger(logger_sock, event_data)
        return True
    except json.JSONDecodeError as e:
        print(f"Error parsing event: {e}")
        return False
    except Exception as e:
        print(f"Error processing event: {e}")
        return False


logger_sock = connect_to_logger()

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Consumer listening for malware events...")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                buffer = ""
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break

                    # Handle newline-delimited JSON
                    buffer += data.decode()
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        if line.strip():
                            process_malware_event(line.strip(), logger_sock)
finally:
    if logger_sock:
        logger_sock.close()
        print("Disconnected from logger")
