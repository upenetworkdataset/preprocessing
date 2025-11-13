import json
import os
import socket
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

HOST = ''
PORT = 6000
BATCH_SIZE = int(os.getenv("LOGGER_BATCH_SIZE", "1000"))

DEFAULT_OUTPUT = Path(os.getenv("LOGGER_OUTPUT_DIR", "/data"))
try:
    DEFAULT_OUTPUT.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR = DEFAULT_OUTPUT
except OSError:
    fallback = Path.cwd() / "logs"
    fallback.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR = fallback

PENDING_FILE = OUTPUT_DIR / "pending.jsonl"


def recover_partial_parquets():
    partial_records = []
    max_full_index = -1
    for path in sorted(OUTPUT_DIR.glob("traffic_log_*.parquet")):
        suffix = path.stem.split("_")[-1]
        try:
            index = int(suffix)
        except ValueError:
            continue
        try:
            parquet_file = pq.ParquetFile(path)
        except (FileNotFoundError, OSError) as err:
            print(f"Skipping unreadable parquet {path.name}: {err}")
            continue
        rows = parquet_file.metadata.num_rows
        if rows < BATCH_SIZE:
            table = parquet_file.read()
            df = table.to_pandas()
            partial_records.extend(df.to_dict(orient="records"))
            path.unlink(missing_ok=True)
            print(f"Recovered {rows} rows from partial {path.name}")
        else:
            max_full_index = max(max_full_index, index)
    return partial_records, max_full_index + 1


def load_pending():
    pending = []
    if PENDING_FILE.exists():
        with PENDING_FILE.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    pending.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        if pending:
            print(f"Loaded {len(pending)} pending rows")
    return pending


def next_file_index(initial_index):
    return max(initial_index, 0)


partial_recovery, starting_index = recover_partial_parquets()
records = load_pending()
if partial_recovery:
    records.extend(partial_recovery)
file_index = next_file_index(starting_index)


def persist_pending():
    if records:
        with PENDING_FILE.open("w", encoding="utf-8") as handle:
            for entry in records:
                handle.write(json.dumps(entry) + "\n")
        print(f"Persisted {len(records)} pending rows")
    elif PENDING_FILE.exists():
        PENDING_FILE.unlink()


def write_parquet(batch, index):
    df = pd.DataFrame(batch)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, str(OUTPUT_DIR / f"traffic_log_{index:04d}.parquet"))
    print(f"Wrote {len(batch)} rows to traffic_log_{index:04d}.parquet")


def flush_batches():
    global file_index
    while len(records) >= BATCH_SIZE:
        write_parquet(records[:BATCH_SIZE], file_index)
        del records[:BATCH_SIZE]
        file_index += 1

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Logger listening...")
        flush_batches()
        persist_pending()
        while True:
            try:
                conn, addr = s.accept()
            except KeyboardInterrupt:
                break
            print(f"Logger connected by {addr}")
            buffer = ""
            with conn:
                while True:
                    try:
                        data = conn.recv(4096)
                    except KeyboardInterrupt:
                        raise
                    if not data:
                        break
                    buffer += data.decode()
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        if not line:
                            continue
                        records.append(json.loads(line))
                        flush_batches()
            if buffer.strip():
                try:
                    records.append(json.loads(buffer))
                    flush_batches()
                except json.JSONDecodeError:
                    print("Discarded incomplete JSON fragment")
            print("Connection closed")
            persist_pending()
except KeyboardInterrupt:
    print("Logger shutting down")
finally:
    persist_pending()

print("Logger finished writing parquet batches")
