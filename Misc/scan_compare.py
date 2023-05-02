#!/usr/bin/env python3

"""
Author: Joseph Erdosy, ChatGPT4
Date: 2023-05-05
Description: This script performs several different types of Nmap scans on a list of 
             hosts and saves the results to a CSV file. You can provide additional
             Nmap flags as command-line arguments after the filename.
             
ADDITIONAL_FLAGS (list): A list of additional Nmap flags to be included in the scan command.
"""

import subprocess
import sys
import os
import time
import socket
import re
import ipaddress
import pandas as pd


# Any arguments to the script after the filename are to be treated like additional nmap flags
ADDITIONAL_FLAGS = sys.argv[2:] if len(sys.argv) > 2 else []

# Define the list of scans to perform as a dictionary
SCAN_TYPES = {
    "Live Host (Ping)": "-sn",
    "Live Host (No Ping)": "-Pn",
    "TCP Connect Scan": "-sT",
    "SYN Scan": "-sS",
    "NULL Scan": "-sN",
    "FIN Scan": "-sF",
    "XMAS Scan": "-sX",
    "ARP Scan": "-PR",
}

def expand_cidr_or_range(host: str) -> list:
    """
    Takes an input string containing an IP address in CIDR notation or as an IP range, 
    and returns a list of individual IP addresses.

    Parameters:
        host (str): The input string containing an IP address in CIDR notation or as an IP range.

    Returns:
        list: A list of individual IP addresses.
    """

    if '/' in host:
        try:
            network = ipaddress.ip_network(host, strict=False)
            return [str(ip) for ip in network.hosts()]
        except ValueError as error:
            print(f"Error parsing CIDR notation {host}: {error}")
            return []
    elif '-' in host:
        try:
            start_ip, end_ip = host.split('-')
            start_ip = ipaddress.ip_address(start_ip.strip())
            if '.' in end_ip:
                end_ip = ipaddress.ip_address(end_ip.strip())
            else:
                end_ip = start_ip + int(end_ip.strip())
            return [str(ip) for ip in range(int(start_ip), int(end_ip)+1)]
        except ValueError as error:
            print(f"Error parsing IP range {host}: {error}")
            return []
    else:
        return [host]

def resolve_dns(host: str) -> str:
    """
    Takes a DNS name as input and returns the corresponding IP address. 
    If the DNS name cannot be resolved, it returns "N/A".

    Parameters:
        host (str): The input string containing a DNS name.

    Returns:
        str: The resolved IP address or "N/A" if the DNS name cannot be resolved.
    """
    try:
        ip_addr = socket.gethostbyname(host)
        return ip_addr
    except socket.gaierror:
        return "N/A"

def process_hosts(hosts_list: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a DataFrame containing hosts as input and processes them to generate a new 
    DataFrame with individual IP addresses.
    For each host, it checks if it is in CIDR notation, an IP range, or a DNS name. 
    It then expands the CIDR notation or range, and resolves the DNS name.

    Parameters:
        hosts (pd.DataFrame): The input DataFrame containing hosts as rows.

    Returns:
        pd.DataFrame: A DataFrame with the processed hosts.
    """
    processed_hosts = []
    for _, row in hosts_list.iterrows():
        host = row[0]
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', host):
            expanded_hosts = expand_cidr_or_range(host)
            processed_hosts.extend(expanded_hosts)
        else:
            ip_addr = resolve_dns(host)
            if ip_addr != "N/A":
                processed_hosts.append(ip_addr)
    return pd.DataFrame(processed_hosts)

def perform_scan(cmd: str, host_list: pd.DataFrame, additional_flags: list=None) -> pd.Series:
    """
    Perform an Nmap scan on a list of hosts and return a Pandas Series with the scan results.
    
    Args:
        cmd (str): The Nmap command-line option for the scan type.
        host_list (pd.DataFrame): A dataframe containing a list of hosts to be scanned.
        additional_flags (list, optional): A list of additional Nmap flags to be included 
                                           in the scan command.
        
    Returns:
        pd.Series: A Pandas Series with boolean values representing the scan results for each host.
    """
    is_up = []
    if additional_flags is None:
        additional_flags = []
    for _, row in host_list.iterrows():
        host = row[0]
        nmap_command = ["nmap", cmd, host] + additional_flags
        try:
            output = subprocess.check_output(nmap_command)
        except subprocess.CalledProcessError as error:
            print(f"Error scanning {host} with command {' '.join(nmap_command)}: "
                  f"{error.output.decode('utf-8').strip()}")
            is_up.append(False)
            continue
        output = output.decode("utf-8")
        if "Host is up" in output:
            is_up.append(True)
        else:
            is_up.append(False)
    return pd.Series(is_up)


# Read the target hosts from a file specified in the command-line argument
if len(sys.argv) < 2:
    print("Usage: scan_compare.py [filename]")
    sys.exit(1)

FILENAME = sys.argv[1]
hosts = pd.read_csv(FILENAME, header=None)

# Process the hosts list
hosts = process_hosts(hosts)

# Disable scans that require root privileges on non-root accounts or that don't work on Windows
if os.geteuid() != 0:
    SCAN_TYPES.pop("NULL Scan")
    SCAN_TYPES.pop("FIN Scan")
    SCAN_TYPES.pop("XMAS Scan")

# Perform the scans for each type of scan and save the results to a dictionary
results = {}
for scan_type, nmap_cmd in SCAN_TYPES.items():
    print(f"Performing {scan_type} scan")
    start_time = time.time()
    results[scan_type] = perform_scan(nmap_cmd, hosts, ADDITIONAL_FLAGS)
    end_time = time.time()
    print(f"Completed {scan_type} scan in {end_time - start_time:.2f} seconds")

# Create a Pandas dataframe with the results and write it to a CSV file
df = pd.concat([hosts, pd.DataFrame(results)], axis=1)
df.columns = ["Host"] + [f"{scan_type} ({arg})" for scan_type, arg in SCAN_TYPES.items()]
df.to_csv("results.csv", index=False)
print("Results saved to results.csv")
