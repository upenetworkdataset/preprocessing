import ipaddress
import json
import random
import socket
import time
from datetime import datetime, timezone

CONSUMER_HOST = "consumer"
CONSUMER_PORT = 5000
SEND_INTERVAL_SECONDS = 0.5
CONNECT_RETRY_DELAY = 1.0
MAX_CONNECT_ATTEMPTS = 120

TCP_FLAGS = ["S", "A", "F", "P", "R"]
CLASS_DISTRIBUTION = [
    ("background", "background", 0.88),
    ("anomaly", "botnet", 0.04),
    ("anomaly", "ddos", 0.03),
    ("anomaly", "scan", 0.03),
    ("anomaly", "spam", 0.02),
]


def _connect_with_retry() -> socket.socket:
    for attempt in range(1, MAX_CONNECT_ATTEMPTS + 1):
        try:
            return socket.create_connection((CONSUMER_HOST, CONSUMER_PORT))
        except OSError:
            time.sleep(CONNECT_RETRY_DELAY)
    raise RuntimeError("Unable to connect to consumer after multiple attempts")


def _choose_flags(proto: str) -> str:
    if proto != "tcp":
        return "."
    count = random.randint(1, len(TCP_FLAGS))
    return "".join(sorted(random.sample(TCP_FLAGS, count)))


def _choose_class() -> tuple[str, str]:
    roll = random.random()
    cumulative = 0.0
    for cls, tag, weight in CLASS_DISTRIBUTION:
        cumulative += weight
        if roll <= cumulative:
            return cls, tag
    return CLASS_DISTRIBUTION[-1][0], CLASS_DISTRIBUTION[-1][1]


def _generate_flow_record() -> dict[str, object]:
    now = datetime.now(timezone.utc)
    proto = random.choice(["tcp", "udp", "icmp"])
    packets = random.randint(1, 2_000)
    bytes_per_packet = random.randint(40, 1_500)
    class_label, tag = _choose_class()

    if proto == "icmp":
        src_port = dst_port = 0
    else:
        src_port = random.randint(1024, 65535)
        dst_port = random.randint(1, 65535)

    return {
        "Date first seen": now.strftime("%Y-%m-%d %H:%M:%S.%f"),
        "Duration": round(random.uniform(0.0001, 300.0), 6),
        "Proto": proto,
        "Src IP Addr": str(ipaddress.IPv4Address(random.getrandbits(32))),
        "Src Pt": src_port,
        "Dst IP Addr": str(ipaddress.IPv4Address(random.getrandbits(32))),
        "Dst Pt": dst_port,
        "Packets": packets,
        "Bytes": packets * bytes_per_packet,
        "Flags": _choose_flags(proto),
        "Tos": random.randint(0, 255),
        "Class": class_label,
        "Tag": tag,
    }


def _stream_records(sock: socket.socket) -> None:
    while True:
        record = _generate_flow_record()
        payload = json.dumps(record, separators=(",", ":")) + "\n"
        sock.sendall(payload.encode("utf-8"))
        time.sleep(SEND_INTERVAL_SECONDS)


def main() -> None:
    while True:
        try:
            with _connect_with_retry() as conn:
                _stream_records(conn)
        except (ConnectionError, OSError):
            time.sleep(CONNECT_RETRY_DELAY)


if __name__ == "__main__":
    main()
