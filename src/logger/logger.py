import socket
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import json
import time

HOST = ''
PORT = 6000

records = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Logger listening...")
    conn, addr = s.accept()
    print(f"Logger connected by {addr}")

    for _ in range(100):  # capture 100 messages, for example
        data = conn.recv(1024)
        if not data:
            break
        for line in data.decode().splitlines():
            records.append(json.loads(line))

df = pd.DataFrame(records)
table = pa.Table.from_pandas(df)
pq.write_table(table, "traffic_log.parquet")
print("Saved to traffic_log.parquet")
