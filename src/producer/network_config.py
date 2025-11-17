"""
Network-secured versions of synthetic malware scripts.
All external IPs/domains are replaced with internal Docker network addresses.
Scripts run as-is but within the isolated msgnet network.
"""

# These will be used by the modified scripts
INTERNAL_TARGETS = {
    # Map external addresses to internal Docker network
    "192.168.0.200": "consumer",
    "192.168.0.100": "consumer",
    "192.168.0.101": "consumer",
    "192.168.0.102": "consumer",
    "192.168.0.103": "consumer",
    "irc.example.com": "consumer",
}


def get_internal_target(external_address):
    """Map external address to internal Docker network address"""
    return INTERNAL_TARGETS.get(external_address, "consumer")
