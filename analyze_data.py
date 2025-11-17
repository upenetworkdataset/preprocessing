"""
Example: Analyzing Synthetic Malware Traffic Data

This script demonstrates how to analyze the generated malware traffic data.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def load_data(data_dir="./data"):
    """Load all parquet files from the data directory"""
    data_path = Path(data_dir)
    parquet_files = list(data_path.glob("traffic_log_*.parquet"))

    if not parquet_files:
        print(f"No parquet files found in {data_dir}")
        return None

    print(f"Found {len(parquet_files)} parquet file(s)")

    # Load all files
    dfs = []
    for file in parquet_files:
        df = pd.read_parquet(file)
        dfs.append(df)

    # Combine all dataframes
    return pd.concat(dfs, ignore_index=True)


def basic_statistics(df):
    """Print basic statistics about the dataset"""
    print("\n=== BASIC STATISTICS ===")
    print(f"Total events: {len(df)}")
    print(f"Time range: {df['datetime'].min()} to {df['datetime'].max()}")
    print(f"Unique source IPs: {df['source_ip'].nunique()}")
    print(f"Unique destination IPs: {df['dest_ip'].nunique()}")


def malware_distribution(df):
    """Analyze malware type distribution"""
    print("\n=== MALWARE TYPE DISTRIBUTION ===")
    counts = df["malware_type"].value_counts()
    percentages = df["malware_type"].value_counts(normalize=True) * 100

    for malware_type in counts.index:
        print(
            f"{malware_type:25s}: {counts[malware_type]:6d} ({percentages[malware_type]:5.2f}%)"
        )


def analyze_attacks(df):
    """Analyze attack patterns"""
    print("\n=== ATTACK ANALYSIS ===")

    # Brute force analysis
    brute_force = df[df["malware_type"].str.contains("bruteforce", na=False)]
    print(f"\nBrute Force Attacks: {len(brute_force)}")
    if len(brute_force) > 0:
        print("  By type:")
        for attack_type in brute_force["malware_type"].unique():
            count = len(brute_force[brute_force["malware_type"] == attack_type])
            print(f"    {attack_type}: {count}")

    # DDoS analysis
    ddos = df[df["malware_type"].str.contains("ddos", na=False)]
    print(f"\nDDoS Attacks: {len(ddos)}")
    if len(ddos) > 0:
        print("  By type:")
        for attack_type in ddos["malware_type"].unique():
            count = len(ddos[ddos["malware_type"] == attack_type])
            print(f"    {attack_type}: {count}")

    # Botnet analysis
    botnet = df[df["malware_type"].str.contains("botnet", na=False)]
    print(f"\nBotnet Activity: {len(botnet)}")
    if len(botnet) > 0:
        print("  By type:")
        for attack_type in botnet["malware_type"].unique():
            count = len(botnet[botnet["malware_type"] == attack_type])
            print(f"    {attack_type}: {count}")


def protocol_analysis(df):
    """Analyze protocol distribution"""
    print("\n=== PROTOCOL ANALYSIS ===")
    protocols = df["protocol"].value_counts()
    for protocol in protocols.index:
        print(f"{protocol:10s}: {protocols[protocol]:6d}")


def port_analysis(df):
    """Analyze most targeted ports"""
    print("\n=== TOP TARGETED PORTS ===")
    top_ports = df["dest_port"].value_counts().head(10)
    for port in top_ports.index:
        count = top_ports[port]
        # Try to identify common ports
        port_names = {
            21: "FTP",
            22: "SSH",
            80: "HTTP",
            443: "HTTPS",
            8080: "HTTP-Alt",
            6667: "IRC",
        }
        port_name = port_names.get(port, "Unknown")
        print(f"Port {port:5d} ({port_name:10s}): {count:6d}")


def time_series_analysis(df):
    """Analyze attack patterns over time"""
    print("\n=== TIME SERIES ANALYSIS ===")

    df["datetime"] = pd.to_datetime(df["datetime"])
    df_time = df.set_index("datetime")

    # Events per minute
    per_minute = df_time.resample("1min").size()
    print(f"Average events per minute: {per_minute.mean():.2f}")
    print(f"Max events per minute: {per_minute.max()}")
    print(f"Min events per minute: {per_minute.min()}")


def top_attackers(df):
    """Find most active source IPs"""
    print("\n=== TOP ATTACKERS (Source IPs) ===")
    top_sources = df["source_ip"].value_counts().head(10)
    for ip in top_sources.index:
        print(f"{ip:15s}: {top_sources[ip]:6d} events")


def top_targets(df):
    """Find most targeted destination IPs"""
    print("\n=== TOP TARGETS (Destination IPs) ===")
    top_dests = df["dest_ip"].value_counts().head(10)
    for ip in top_dests.index:
        print(f"{ip:15s}: {top_dests[ip]:6d} events")


def export_summary(df, output_file="analysis_summary.txt"):
    """Export analysis summary to file"""
    import sys

    # Redirect stdout to file
    original_stdout = sys.stdout
    with open(output_file, "w") as f:
        sys.stdout = f

        basic_statistics(df)
        malware_distribution(df)
        analyze_attacks(df)
        protocol_analysis(df)
        port_analysis(df)
        time_series_analysis(df)
        top_attackers(df)
        top_targets(df)

    sys.stdout = original_stdout
    print(f"\nAnalysis summary exported to {output_file}")


def plot_malware_distribution(df):
    """Create a pie chart of malware distribution"""
    counts = df["malware_type"].value_counts()

    plt.figure(figsize=(10, 8))
    plt.pie(counts.values, labels=counts.index, autopct="%1.1f%%")
    plt.title("Malware Type Distribution")
    plt.tight_layout()
    plt.savefig("malware_distribution.png")
    print("Saved plot: malware_distribution.png")


def plot_timeline(df):
    """Create a timeline of attack activity"""
    df["datetime"] = pd.to_datetime(df["datetime"])
    df_time = df.set_index("datetime")

    # Events per minute by malware type
    malware_types = df["malware_type"].unique()

    plt.figure(figsize=(14, 8))
    for malware_type in malware_types:
        subset = df_time[df_time["malware_type"] == malware_type]
        per_minute = subset.resample("1min").size()
        plt.plot(per_minute.index, per_minute.values, label=malware_type, alpha=0.7)

    plt.title("Attack Activity Timeline")
    plt.xlabel("Time")
    plt.ylabel("Events per Minute")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig("attack_timeline.png")
    print("Saved plot: attack_timeline.png")


def main():
    """Main analysis function"""
    print("=" * 60)
    print("SYNTHETIC MALWARE TRAFFIC ANALYSIS")
    print("=" * 60)

    # Load data
    df = load_data()
    if df is None:
        return

    # Run analyses
    basic_statistics(df)
    malware_distribution(df)
    analyze_attacks(df)
    protocol_analysis(df)
    port_analysis(df)
    time_series_analysis(df)
    top_attackers(df)
    top_targets(df)

    # Export summary
    export_summary(df)

    # Create plots (if matplotlib is available)
    try:
        plot_malware_distribution(df)
        plot_timeline(df)
    except Exception as e:
        print(f"\nNote: Could not create plots: {e}")

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
