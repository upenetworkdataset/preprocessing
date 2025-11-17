"""
Traffic generator that sends both malicious and normal traffic events to consumer.
This bridges the secured malware scripts with the consumer's JSON event format.
"""

import socket
import json
import time
import random
import threading
from datetime import datetime

CONSUMER_HOST = "consumer"
CONSUMER_PORT = 5000


def connect_to_consumer():
    """Establish connection to consumer service"""
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((CONSUMER_HOST, CONSUMER_PORT))
            print(
                f"[TrafficGen] Connected to consumer at {CONSUMER_HOST}:{CONSUMER_PORT}"
            )
            return sock
        except (socket.error, ConnectionRefusedError) as e:
            print(
                f"[TrafficGen] Cannot connect to consumer: {e}. Retrying in 5 seconds..."
            )
            time.sleep(5)


def send_event(sock, event):
    """Send a JSON event to consumer"""
    try:
        sock.sendall((json.dumps(event) + "\n").encode())
        return True
    except (socket.error, BrokenPipeError) as e:
        print(f"[TrafficGen] Error sending event: {e}")
        return False


def generate_malicious_beaconing(sock):
    """Generate botnet beaconing traffic"""
    print("[TrafficGen] Starting beaconing traffic...")
    while True:
        event = {
            "timestamp": time.time(),
            "malware_type": "beaconing",
            "source_ip": "172.20.0.2",
            "dest_ip": "consumer",
            "source_port": random.randint(40000, 65000),
            "dest_port": 5000,
            "protocol": "TCP",
            "packet_size": random.randint(200, 500),
            "payload": {"bot_id": random.randint(1000, 9999), "status": "online"},
            "traffic_class": "malicious",
            "attack_type": "botnet_c2",
        }
        send_event(sock, event)
        time.sleep(random.randint(10, 30))


def generate_malicious_http_flood(sock):
    """Generate HTTP flood/DDoS traffic"""
    print("[TrafficGen] Starting HTTP flood traffic...")
    while True:
        for _ in range(random.randint(20, 50)):
            event = {
                "timestamp": time.time(),
                "malware_type": "http_flood",
                "source_ip": "172.20.0.2",
                "dest_ip": "consumer",
                "source_port": random.randint(40000, 65000),
                "dest_port": 80,
                "protocol": "TCP",
                "packet_size": random.randint(100, 300),
                "payload": {"method": "GET", "path": f"/?{random.randint(1000, 9999)}"},
                "traffic_class": "malicious",
                "attack_type": "ddos_http",
            }
            send_event(sock, event)
            time.sleep(0.1)
        time.sleep(random.randint(30, 60))


def generate_malicious_bruteforce(sock):
    """Generate brute force attack traffic"""
    print("[TrafficGen] Starting brute force traffic...")
    services = [
        ("ssh_bruteforce", 22, "SSH"),
        ("ftp_bruteforce", 21, "FTP"),
        ("http_bruteforce", 5000, "HTTP"),
    ]

    while True:
        service_type, port, proto = random.choice(services)
        for attempt in range(random.randint(10, 30)):
            event = {
                "timestamp": time.time(),
                "malware_type": service_type,
                "source_ip": "172.20.0.2",
                "dest_ip": "consumer",
                "source_port": random.randint(40000, 65000),
                "dest_port": port,
                "protocol": "TCP",
                "packet_size": random.randint(100, 400),
                "payload": {
                    "username": random.choice(["admin", "root", "user", "test"]),
                    "password": f"pass{random.randint(1000, 9999)}",
                    "attempt": attempt,
                },
                "traffic_class": "malicious",
                "attack_type": "brute_force",
            }
            send_event(sock, event)
            time.sleep(random.uniform(0.5, 2.0))
        time.sleep(random.randint(40, 80))


def generate_malicious_syn_flood(sock):
    """Generate SYN flood traffic"""
    print("[TrafficGen] Starting SYN flood traffic...")
    while True:
        for _ in range(random.randint(50, 100)):
            event = {
                "timestamp": time.time(),
                "malware_type": "syn_flood",
                "source_ip": f"172.20.0.{random.randint(10, 250)}",
                "dest_ip": "consumer",
                "source_port": random.randint(1024, 65000),
                "dest_port": 80,
                "protocol": "TCP",
                "flags": "SYN",
                "packet_size": 54,
                "traffic_class": "malicious",
                "attack_type": "ddos_syn",
            }
            send_event(sock, event)
            time.sleep(0.05)
        time.sleep(random.randint(60, 120))


def generate_malicious_udp_flood(sock):
    """Generate UDP flood traffic"""
    print("[TrafficGen] Starting UDP flood traffic...")
    while True:
        for _ in range(random.randint(50, 100)):
            event = {
                "timestamp": time.time(),
                "malware_type": "udp_flood",
                "source_ip": f"172.20.0.{random.randint(10, 250)}",
                "dest_ip": "consumer",
                "source_port": random.randint(1024, 65000),
                "dest_port": random.randint(1024, 65000),
                "protocol": "UDP",
                "packet_size": random.randint(512, 1024),
                "traffic_class": "malicious",
                "attack_type": "ddos_udp",
            }
            send_event(sock, event)
            time.sleep(0.05)
        time.sleep(random.randint(60, 120))


def generate_normal_web_browsing(sock):
    """Generate normal HTTP web browsing traffic"""
    print("[TrafficGen] Starting normal web browsing traffic...")
    while True:
        event = {
            "timestamp": time.time(),
            "malware_type": "normal_http",
            "source_ip": "172.20.0.2",
            "dest_ip": "consumer",
            "source_port": random.randint(40000, 65000),
            "dest_port": 80,
            "protocol": "TCP",
            "packet_size": random.randint(300, 1500),
            "payload": {
                "method": "GET",
                "path": random.choice(
                    ["/", "/about", "/contact", "/products", "/api/data"]
                ),
                "user_agent": "Mozilla/5.0",
            },
            "traffic_class": "benign",
            "attack_type": None,
        }
        send_event(sock, event)
        time.sleep(random.randint(5, 15))


def generate_normal_dns(sock):
    """Generate normal DNS query traffic"""
    print("[TrafficGen] Starting normal DNS traffic...")
    while True:
        event = {
            "timestamp": time.time(),
            "malware_type": "normal_dns",
            "source_ip": "172.20.0.2",
            "dest_ip": "consumer",
            "source_port": random.randint(40000, 65000),
            "dest_port": 53,
            "protocol": "UDP",
            "packet_size": random.randint(60, 120),
            "payload": {
                "query": random.choice(
                    [
                        "www.example.com",
                        "api.service.com",
                        "cdn.assets.com",
                        "mail.company.com",
                    ]
                )
            },
            "traffic_class": "benign",
            "attack_type": None,
        }
        send_event(sock, event)
        time.sleep(random.randint(10, 30))


def generate_normal_ssh(sock):
    """Generate normal SSH connection traffic"""
    print("[TrafficGen] Starting normal SSH traffic...")
    while True:
        # Successful SSH session
        event = {
            "timestamp": time.time(),
            "malware_type": "normal_ssh",
            "source_ip": "172.20.0.2",
            "dest_ip": "consumer",
            "source_port": random.randint(40000, 65000),
            "dest_port": 22,
            "protocol": "TCP",
            "packet_size": random.randint(200, 800),
            "payload": {"auth": "success", "user": "admin"},
            "traffic_class": "benign",
            "attack_type": None,
        }
        send_event(sock, event)
        time.sleep(random.randint(120, 300))


def generate_normal_ftp(sock):
    """Generate normal FTP transfer traffic"""
    print("[TrafficGen] Starting normal FTP traffic...")
    while True:
        event = {
            "timestamp": time.time(),
            "malware_type": "normal_ftp",
            "source_ip": "172.20.0.2",
            "dest_ip": "consumer",
            "source_port": random.randint(40000, 65000),
            "dest_port": 21,
            "protocol": "TCP",
            "packet_size": random.randint(500, 2000),
            "payload": {"command": "RETR", "file": "data.csv"},
            "traffic_class": "benign",
            "attack_type": None,
        }
        send_event(sock, event)
        time.sleep(random.randint(180, 400))


def main():
    """Main traffic generator"""
    print("=" * 70)
    print("TRAFFIC GENERATOR - Malicious & Normal Traffic")
    print("=" * 70)

    # Connect to consumer
    sock = connect_to_consumer()

    # Start all traffic generators in separate threads
    generators = [
        # Malicious traffic
        generate_malicious_beaconing,
        generate_malicious_http_flood,
        generate_malicious_bruteforce,
        generate_malicious_syn_flood,
        generate_malicious_udp_flood,
        # Normal traffic
        generate_normal_web_browsing,
        generate_normal_dns,
        generate_normal_ssh,
        generate_normal_ftp,
    ]

    threads = []
    for gen_func in generators:
        thread = threading.Thread(target=gen_func, args=(sock,), daemon=True)
        thread.start()
        threads.append(thread)
        time.sleep(1)

    print("\n[TrafficGen] All traffic generators running")
    print("[TrafficGen] Sending both malicious and benign traffic...")
    print("[TrafficGen] Press Ctrl+C to stop\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[TrafficGen] Stopping...")
        sock.close()


if __name__ == "__main__":
    main()
