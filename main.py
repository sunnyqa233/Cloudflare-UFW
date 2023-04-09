import subprocess
import requests
import time
import os
import re

"""
Settings
"""
comment = "cloudflare-ufw-managed"  # Only change this if you know what you're doing

enable_ipv4 = True
ipv4_list_url = "https://www.cloudflare.com/ips-v4"
ipv4_tcp_ports = [80, 443]
ipv4_udp_ports = [443]

enable_ipv6 = True
ipv6_list_url = "https://www.cloudflare.com/ips-v6"
ipv6_tcp_ports = [80, 443]
ipv6_udp_ports = [443]

"""
Checks
"""
# Run as root
if os.geteuid() != 0:
    print("Please run this script as root.", )
    time.sleep(5)
    exit(1)

# UFW exists in path and running
try:
    result = subprocess.run(["ufw", "status"], capture_output=True)
    if "Status: inactive" in result.stdout.decode("utf-8"):
        print("UFW is inactive.", )
        time.sleep(5)
        exit(1)
except FileNotFoundError:
    print("UFW not installed or UFW not in PATH.", )
    time.sleep(5)
    exit(1)

# This script can't be edited by non-root user
file_protection_mode = oct(os.stat(__file__).st_mode)
if file_protection_mode[-3:] != "644":
    print("Please make sure this script's permission is set to 644.", )

"""
Add rules
"""
cloudflare_ipv4_list = requests.get(ipv4_list_url).text.split("\n")
cloudflare_ipv6_list = requests.get(ipv6_list_url).text.split("\n")
if enable_ipv4:

    for port in ipv4_tcp_ports:
        for ip in cloudflare_ipv4_list:
            command = f"ufw allow proto tcp from {ip} to any port {port} comment '{comment}'"
            print(command)
            os.system(command)

    for port in ipv4_udp_ports:
        for ip in cloudflare_ipv4_list:
            command = f"ufw allow proto udp from {ip} to any port {port} comment '{comment}'"
            print(command)
            os.system(command)


if enable_ipv6:

    for port in ipv6_tcp_ports:
        for ip in cloudflare_ipv6_list:
            command = f"ufw allow proto tcp from {ip} to any port {port} comment '{comment}'"
            print(command)
            os.system(command)

    for port in ipv6_udp_ports:
        for ip in cloudflare_ipv6_list:
            command = f"ufw allow proto udp from {ip} to any port {port} comment '{comment}'"
            print(command)
            os.system(command)

"""
Parse UFW status
"""
ufw_status = subprocess.run(["ufw", "status"], capture_output=True).stdout.decode("utf-8", errors="ignore")

existing_rules = []
# Parse existing rules
for raw_rule in ufw_status.split("\n"):
    if f'# {comment}' in raw_rule:  # Is managed raw_rules
        # IP
        is_ipv4 = True
        ip = re.search(r"\d+\.\d+\.\d+\.\d+/\d+", raw_rule)  # Match IPV4 CIDR
        if not ip:
            is_ipv4 = False
            ip = re.search(r".{4}:.{4}::/\d{2,}", raw_rule)  # Match IPV6 CIDR
        ip = ip.group()
        # Port & Protocol
        port, protocol = re.search(r"\d+/((tcp)|(udp))", raw_rule).group().split("/")
        # Add item
        existing_rules.append(
            {
                "proto": protocol,
                "port": port,
                "ip": ip,
                "ipv4": is_ipv4
            }
        )

outdated_rules = []
for rule in existing_rules:
    # Is IPV4 rule
    if rule["ipv4"]:
        # IPV4 disabled
        if not enable_ipv4:
            outdated_rules.append(rule)
        # Outdated cloudflare IP
        elif rule["ip"] not in cloudflare_ipv4_list:  # Match IP
            outdated_rules.append(
                rule
            )
        # Non-listed TCP port
        elif rule["proto"] == "tcp":
            if int(rule["port"]) not in ipv4_tcp_ports:
                outdated_rules.append(
                    rule
                )
        # Non-listed UDP port
        elif rule["proto"] == "udp":
            if int(rule["port"]) not in ipv4_udp_ports:
                outdated_rules.append(
                    rule
                )
    # Is IPV6 rule
    else:
        # IPV6 disabled
        if not enable_ipv6:
            outdated_rules.append(rule)
        # Outdated cloudflare IP
        elif rule["ip"] not in cloudflare_ipv6_list:
            outdated_rules.append(
                rule
            )
        # Non-listed TCP port
        elif rule["proto"] == "tcp":
            if int(rule["port"]) not in ipv6_tcp_ports:
                outdated_rules.append(
                    rule
                )
        # Non-listed UDP port
        elif rule["proto"] == "udp":
            if int(rule["port"]) not in ipv6_udp_ports:
                outdated_rules.append(
                    rule
                )


"""
Remove outdated rules
"""
for rule in outdated_rules:
    command = f"ufw delete allow proto {rule['proto']} from {rule['ip']} to any port {rule['port']}"
    print(command)
    os.system(command)
