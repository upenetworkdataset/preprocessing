# preprocessing

Pre-processing scripts for network data using Docker containers with producer-consumer architecture.

## Overview

This project implements a distributed data processing pipeline with three main components:

- **Producer**: Generates sample network traffic data (timestamp + random value)
- **Consumer**: Receives and displays data from the producer
- **Logger**: Captures network data and saves it to Parquet format

## Prerequisites

- Docker and Docker Compose installed
- Python 3.13+ (if running locally without Docker)

## Setup

### 1. Create the Docker Network

Before running the services, create the external Docker network:

```bash
docker network create msgnet
```

### 2. Build and Run with Docker Compose

Build and start all services:

```bash
docker-compose up --build
```

To run in detached mode (background):

```bash
docker-compose up -d --build
```

### 3. View Logs

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

1. The **producer** will automatically start sending data to the consumer every second
2. The **consumer** will receive and display the data
3. The **logger** will capture 100 messages and save them to `/data/traffic_log.parquet`

### Accessing Output Data

The logger saves data to a Parquet file in the `./data` directory (mounted as a volume). You can access the output file at:

```text
./data/traffic_log.parquet
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
│   └── ugr16_simulated/       # Sample data directory
└── src/
    ├── producer/
    │   ├── Dockerfile
    │   └── producer.py         # Generates and sends data
    ├── consumer/
    │   ├── Dockerfile
    │   └── consumer.py         # Receives and displays data
    └── logger/
        ├── Dockerfile
        └── logger.py           # Logs data to Parquet format
```

## Dependencies

- pandas >= 2.3.3
- pyarrow >= 22.0.0

These are automatically installed in the Docker containers during build.

## Troubleshooting

### Network Issues

If you encounter network connection errors, ensure the `msgnet` network exists:

```bash
docker network ls
docker network create msgnet
```

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
