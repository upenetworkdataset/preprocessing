import json
import socket
import time
import uuid
from pathlib import Path
from typing import Dict, List

import pyarrow as pa
import pyarrow.parquet as pq

HOST = ""
PORT = 6000
BUFFER_SIZE = 4096
FLUSH_BATCH_SIZE = 50
FLUSH_INTERVAL_SECONDS = 5.0
OUTPUT_DIR = Path("/data/ugr16_simulated")

SCHEMA = pa.schema(
    [
        ("Date first seen", pa.string()),
        ("Duration", pa.float32()),
        ("Proto", pa.string()),
        ("Src IP Addr", pa.string()),
        ("Src Pt", pa.int32()),
        ("Dst IP Addr", pa.string()),
        ("Dst Pt", pa.int32()),
        ("Packets", pa.int32()),
        ("Bytes", pa.int64()),
        ("Flags", pa.string()),
        ("Tos", pa.int32()),
        ("Class", pa.string()),
        ("Tag", pa.string()),
    ]
)


def _sanitize(record: Dict[str, object]) -> Dict[str, object]:
    return {
        "Date first seen": str(record.get("Date first seen", "")),
        "Duration": float(record.get("Duration", 0.0)),
        "Proto": str(record.get("Proto", "")),
        "Src IP Addr": str(record.get("Src IP Addr", "")),
        "Src Pt": int(record.get("Src Pt", 0)),
        "Dst IP Addr": str(record.get("Dst IP Addr", "")),
        "Dst Pt": int(record.get("Dst Pt", 0)),
        "Packets": int(record.get("Packets", 0)),
        "Bytes": int(record.get("Bytes", 0)),
        "Flags": str(record.get("Flags", ".")),
        "Tos": int(record.get("Tos", 0)),
        "Class": str(record.get("Class", "background")),
        "Tag": str(record.get("Tag", "background")),
    }


def _flush(records: List[Dict[str, object]]) -> None:
    if not records:
        return

    table = pa.Table.from_pylist(records, schema=SCHEMA)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    file_path = OUTPUT_DIR / f"ugr16_{int(time.time())}_{uuid.uuid4().hex}.parquet"
    pq.write_table(table, file_path)
    records.clear()


def main() -> None:
    records: List[Dict[str, object]] = []
    buffer = ""
    last_flush = time.monotonic()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print("Logger listening...")
        conn, addr = s.accept()
        print(f"Logger connected by {addr}")

        try:
            with conn:
                while True:
                    chunk = conn.recv(BUFFER_SIZE)
                    if not chunk:
                        break
                    buffer += chunk.decode("utf-8")

                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        if not line.strip():
                            continue
                        try:
                            record = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        records.append(_sanitize(record))
                        if (
                            len(records) >= FLUSH_BATCH_SIZE
                            or time.monotonic() - last_flush >= FLUSH_INTERVAL_SECONDS
                        ):
                            _flush(records)
                            last_flush = time.monotonic()
        finally:
            _flush(records)
            print(f"Saved flows to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
