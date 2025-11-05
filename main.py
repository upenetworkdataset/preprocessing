from pathlib import Path

import pandas as pd

DATA_DIR = Path("data/ugr16_simulated")

if not DATA_DIR.exists():
	raise FileNotFoundError(f"No parquet directory found at {DATA_DIR}")

files = sorted(DATA_DIR.glob("*.parquet"))
if not files:
	raise FileNotFoundError(f"No parquet files present under {DATA_DIR}")

df = pd.concat((pd.read_parquet(path) for path in files))
print(df.head())