# Network Traffic Preprocessing - Synthetic Malware Dataset Generator

Pre-processing pipeline for generating synthetic network traffic data (malicious + benign) using Docker containers with producer-consumer architecture.

## Overview

This project implements a distributed data processing pipeline that generates **both malicious and normal network traffic** with **guaranteed network isolation**. All traffic is properly labeled and stored in Parquet format for machine learning and security research.

### Components

- **Producer**: Generates synthetic malicious attacks AND normal/background network traffic
- **Consumer**: Receives, logs, and forwards all traffic events to logger
- **Logger**: Stores all traffic data in Apache Parquet format with proper labels

### Security Features

✅ **Completely Isolated**: Docker network set to `internal: true` (no external routing)  
✅ **Address Replacement**: All targets point to internal Docker network only  
✅ **Dual Traffic**: Both malicious attacks and normal benign traffic  
✅ **Properly Labeled**: Each event tagged as "malicious" or "benign"  
✅ **Non-Root Containers**: All services run as unprivileged users (UID 1000)  
✅ **Minimal Privileges**: Containers drop all capabilities (`cap_drop: ALL`)  

## Traffic Types Generated

### Malicious Traffic (5 types)

| Type | Description | Frequency |
|------|-------------|-----------|
| **Beaconing** | Botnet C2 communication | Every 10-30 seconds |
| **HTTP Flood** | DDoS attack (HTTP GET requests) | Bursts of 20-50 requests |
| **Brute Force** | SSH/FTP/HTTP login attempts | 10-30 attempts per session |
| **SYN Flood** | TCP SYN flood attack | Bursts of 50-100 packets |
| **UDP Flood** | UDP flood attack | Bursts of 50-100 packets |

### Normal/Benign Traffic (4 types)

| Type | Description | Frequency |
|------|-------------|-----------|
| **Web Browsing** | Normal HTTP GET requests | Every 5-15 seconds |
| **DNS Queries** | Legitimate DNS lookups | Every 10-30 seconds |
| **SSH** | Normal SSH connections | Every 2-5 minutes |
| **FTP** | Legitimate file transfers | Every 3-7 minutes |

## Original Malware Scripts (Reference)

The malicious traffic is inspired by scripts from the [synthetic-malwares submodule](https://github.com/upenetworkdataset/synthetic-malwares):
|----------|------|-------------|
| **Botnet** | Beaconing | Periodic C2 check-ins |
| **Botnet** | IRC C2 | IRC-based command & control |
| **Brute Force** | FTP | Login attempts against FTP |
| **Brute Force** | HTTP | Web form brute forcing |
| **Brute Force** | SSH | SSH authentication attacks |
| **DDoS** | HTTP Flood | High-volume HTTP requests |
| **DDoS** | SYN Flood | TCP SYN packet floods |
| **DDoS** | UDP Flood | UDP packet floods |
| **Normal** | Benign Traffic | Baseline traffic for comparison |

## Prerequisites

- Docker and Docker Compose installed
- Python 3.13+ (if running locally without Docker)

## Setup

### 1. Build and Run with Docker Compose

Build and start all services:

```bash
docker-compose up --build
```

To run in detached mode (background):

```bash
docker-compose up -d --build
```

### 2. View Logs

To view logs from all services:

```bash
docker-compose logs -f
```

To view logs from a specific service:

```bash
docker-compose logs -f producer
docker-compose logs -f consumer
docker-compose logs -f logger
```

## Usage

### Running the Services

Once the services are running:

1. The **producer** will simulate various malware traffic patterns
2. The **consumer** will receive and process the synthetic malware events
3. The **logger** will capture events and save them to Parquet format in `/data/`

### Sample Output

The producer generates events like:

```json
{
  "timestamp": 1700000000.123,
  "datetime": "2023-11-14T12:00:00.123456",
  "malware_type": "bruteforce_ssh",
  "source_ip": "10.0.0.45",
  "dest_ip": "10.0.0.101",
  "dest_port": 22,
  "protocol": "SSH",
  "username": "admin",
  "password_attempt": "123456",
  "attempt_number": 1,
  "success": false
}
```

### Accessing Output Data

The logger saves data to Parquet files in the `./data` directory (mounted as a volume):

```text
./data/traffic_log_*.parquet
```

You can analyze this data using pandas:

```python
import pandas as pd

# Read the parquet file
df = pd.read_parquet('./data/traffic_log_0.parquet')

# View malware type distribution
print(df['malware_type'].value_counts())

# Filter by attack type
ssh_attacks = df[df['malware_type'] == 'bruteforce_ssh']
```

### Stopping the Services

To stop all services:

```bash
docker-compose down
```

To stop and remove volumes:

```bash
docker-compose down -v
```

## Project Structure

```text
preprocessing/
├── docker-compose.yml          # Docker Compose configuration
├── pyproject.toml              # Python project configuration
├── README.md                   # This file
├── data/                       # Output directory for logged data
└── src/
    ├── producer/
    │   ├── Dockerfile
    │   ├── producer.py         # Synthetic malware simulator
    │   ├── SECURITY.md         # Security documentation
    │   └── synthetic-malwares/ # Reference implementations (submodule)
    ├── consumer/
    │   ├── Dockerfile
    │   └── consumer.py         # Event processor
    └── logger/
        ├── Dockerfile
        └── logger.py           # Data logger
```

## Dependencies

- pandas >= 2.3.3
- pyarrow >= 22.0.0

These are automatically installed in the Docker containers during build.

## Security & Ethics

⚠️ **IMPORTANT NOTICE**

This tool is designed for:
- Network security research
- IDS/IPS testing and development
- Machine learning dataset generation
- Educational purposes in controlled environments

**DO NOT:**
- Use against systems you don't own or have explicit permission to test
- Deploy on networks with external connectivity
- Modify to perform actual attacks
- Remove or bypass security constraints

See `src/producer/SECURITY.md` for detailed security documentation.

## Use Cases

### 1. Training IDS/IPS Systems
Generate labeled datasets with various attack patterns for training intrusion detection systems.

### 2. Testing Security Tools
Validate your network monitoring and security analytics tools against known attack patterns.

### 3. Research & Development
Study malware behavior patterns and develop detection algorithms.

### 4. Machine Learning
Create labeled datasets for supervised learning models in cybersecurity.

## Dataset Format

Each event contains:
- **timestamp**: Unix timestamp
- **datetime**: ISO 8601 datetime string
- **malware_type**: Classification of the attack/traffic type
- **source_ip**: Simulated source IP address
- **dest_ip**: Simulated destination IP address  
- **dest_port**: Target port number
- **protocol**: Network protocol (HTTP, SSH, FTP, etc.)
- **[attack-specific fields]**: Additional metadata based on malware type

## References

Based on synthetic malware implementations from:
- [UPE Network Dataset - Synthetic Malwares](https://github.com/upenetworkdataset/synthetic-malwares)

## Troubleshooting

### Network Issues

The Docker Compose file now creates an isolated internal network automatically. No manual network creation needed.

### Port Conflicts

The services use the following internal ports:

- Consumer: 5000
- Logger: 6000

If you need to expose these ports to the host, modify the `docker-compose.yml` file.

### Rebuilding Containers

If you make changes to the code, rebuild the containers:

```bash
docker-compose up --build
```
