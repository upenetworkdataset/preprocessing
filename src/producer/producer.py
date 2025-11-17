"""
Producer that generates both malicious and normal network traffic.
Uses traffic_generator.py which sends JSON events to consumer.
Consumer forwards all traffic to logger for storage.
"""

import subprocess
import sys


def main():
    """Main producer function"""
    print("=" * 70)
    print("NETWORK TRAFFIC PRODUCER")
    print("Generating synthetic malicious and normal traffic")
    print("=" * 70)
    print()
    print("TRAFFIC TYPES:")
    print("  Malicious:")
    print("    • Botnet beaconing (C2 communication)")
    print("    • HTTP flood (DDoS)")
    print("    • Brute force (SSH, FTP, HTTP)")
    print("    • SYN flood (DDoS)")
    print("    • UDP flood (DDoS)")
    print()
    print("  Normal/Benign:")
    print("    • Web browsing (HTTP)")
    print("    • DNS queries")
    print("    • SSH connections")
    print("    • FTP transfers")
    print()
    print("SECURITY GUARANTEES:")
    print("  ✓ All traffic targets internal Docker network only")
    print("  ✓ Network isolated by docker-compose (internal: true)")
    print("  ✓ No external network access possible")
    print()
    print("DATA FLOW:")
    print("  Producer → Consumer → Logger → Parquet files")
    print()
    print("=" * 70)
    print()

    # Run the traffic generator
    try:
        subprocess.run([sys.executable, "traffic_generator.py"], check=True)
    except KeyboardInterrupt:
        print("\n[Producer] Stopped.\n")
    except Exception as e:
        print(f"[Producer] Error: {e}")


if __name__ == "__main__":
    main()
