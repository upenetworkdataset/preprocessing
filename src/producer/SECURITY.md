# Security Documentation for Synthetic Malware Producer

## Overview

This producer uses **adapted modules** from the `synthetic-malwares` submodule to simulate malware traffic patterns for research and testing purposes. The original scripts have been wrapped in adapter classes that capture their behavior patterns and send metadata to the consumer **instead of performing actual attacks**.

**All traffic is safely contained within the Docker network and does not affect external systems.**

## Implementation Approach

### Adapter Pattern
- Original malware scripts from `synthetic-malwares/` are studied for their behavior patterns
- Adapter classes in `malware_adapters.py` replicate these patterns
- Adapters send JSON metadata to consumer instead of executing actual attacks
- No external dependencies required (requests, paramiko, scapy, etc.)

### What is Adapted

| Original Script | Adapter Class | Behavior Captured |
|----------------|---------------|-------------------|
| `BotNet/Beaconing.py` | `BeaconingAdapter` | C2 check-in intervals, bot IDs, HTTP POST patterns |
| `BotNet/C2IRC.py` | `C2IRCAdapter` | IRC connection, PRIVMSG, channel behavior |
| `BruteForce/FtpBruteForce.py` | `FtpBruteForceAdapter` | Password list iteration, timing patterns |
| `BruteForce/HTTPBruteForce.py` | `HTTPBruteForceAdapter` | Login POST requests, response patterns |
| `BruteForce/SshBruteForce.py` | `SSHBruteForceAdapter` | SSH authentication attempts, timeouts |
| `ddos/HttpFlood.py` | `HTTPFloodAdapter` | Request bursts, User-Agent rotation |
| `ddos/SynFlood.py` | `SYNFloodAdapter` | SYN packet patterns, IP spoofing patterns |
| `ddos/UdpFlood.py` | `UDPFloodAdapter` | UDP burst patterns, payload sizes |

## Security Measures

### 1. Network Isolation

- All traffic is restricted to the `msgnet` Docker network
- No external network access from the producer container
- Target IPs are simulated (10.0.0.x range) and not real destinations

### 2. Safe Simulation

- **NO ACTUAL ATTACKS** are performed
- Only generates metadata and traffic patterns
- No real brute force attempts against live systems
- No actual DDoS attacks executed
- No real C2 connections established

### 3. What is Simulated

The producer simulates the following malware patterns:

#### Botnet Behavior

- **Beaconing**: Periodic check-ins to C2 servers
- **IRC C2**: IRC-based command and control communication

#### Brute Force Attacks

- **FTP**: Login attempts against FTP services
- **HTTP**: Web login form attacks
- **SSH**: SSH authentication attempts

#### DDoS Attacks

- **HTTP Flood**: High-volume HTTP requests
- **SYN Flood**: TCP SYN packet floods
- **UDP Flood**: UDP packet floods

#### Normal Traffic

- Benign HTTP/HTTPS traffic for baseline comparison

## Data Generated

Each simulated event includes:

- Timestamp (Unix time and ISO format)
- Malware type classification
- Source and destination IPs (simulated)
- Port numbers and protocols
- Attack-specific metadata (passwords attempted, request rates, etc.)

## Usage

### Running the Producer

```bash
# Build and start services
docker-compose up --build

# View producer logs
docker-compose logs -f producer

# View consumer logs
docker-compose logs -f consumer
```

### Stopping the Producer

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Network Architecture

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Producer   │────────>│   Consumer   │────────>│    Logger    │
│  (Simulate)  │ msgnet  │  (Process)   │ msgnet  │   (Store)    │
└──────────────┘         └──────────────┘         └──────────────┘
```

## Ethical Considerations

⚠️ **IMPORTANT**: This tool is designed for:

- Network security research
- IDS/IPS testing
- Machine learning model training
- Educational purposes

**DO NOT**:

- Use against systems you don't own or have permission to test
- Deploy on networks with external connectivity
- Modify to perform actual attacks
- Remove security constraints

## Dataset Generation

The synthetic malware data can be used to:

1. Train intrusion detection systems
2. Test network monitoring tools
3. Benchmark security analytics
4. Create labeled datasets for ML models

## Compliance

Ensure you have proper authorization before:

- Running this on any network
- Collecting network traffic data
- Sharing generated datasets

## References

Based on synthetic malwares from:

- https://github.com/upenetworkdataset/synthetic-malwares

## License

See LICENSE file in the root directory.
