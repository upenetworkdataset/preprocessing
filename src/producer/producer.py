import socket
import time
import json
import random

HOST = 'consumer'  # service name on Docker network
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    time.sleep(2)  # wait for consumer to start
    s.connect((HOST, PORT))
    while True:
        msg = {
            "timestamp": time.time(),
            "value": random.random()
        }
        s.sendall((json.dumps(msg) + "\n").encode())
        time.sleep(1)
