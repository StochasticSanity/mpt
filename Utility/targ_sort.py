#!/usr/bin/env python
"""
Script Name: targ-sort.py
Author: Joseph Erdosy (@StochasticSanity)
Date: 05/04/2021

Extracts IP addresses, URLs, and CIDR ranges from files matching the "targ-*" pattern
in the current directory.

Outputs:
- One file containing IP addresses found in each input file
- One file containing URLs, domains, and subdomains found in each input file
- One file containing CIDR and IP ranges found in each input file

Notes:
- This script assumes that the input files are in plain text format. If the files are in a binary
format, you may need to modify the script to use a different method for reading the file contents.
- If any of the extracted values are empty, no output file is created for that type of value.
- Each value is written to a separate line in the output file.
"""

import os
import re

IP_RANGE_REGEX = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:-\d{1,3}(?:\.\d{1,3}){0,3}|\b\/\d{1,2}\b)"
IP_REGEX = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
IPV6_REGEX = r"\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b"

def punycode_domain(domain):
    """
    Convert a domain to its punycode representation.

    Arguments:
        domain (str): Domain to be converted.

    Returns:
        str: Punycode representation of the domain.
    """
    return ".".join([part.encode("idna").decode("ascii") for part in domain.split(".")])

def is_valid_domain(domain):
    """
    Check if the domain is valid.

    Arguments:
        domain (str): Domain to be checked.

    Returns:
        bool: True if the domain is valid, False otherwise.
    """
    if len(domain) > 253:
        return False
    domain_parts = domain.split(".")
    if any(len(part) > 63 for part in domain_parts):
        return False

    valid_label = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$")
    return all(valid_label.match(part) for part in domain_parts)

def extract_data(file_name):
    """
    Extract IP addresses, URLs, and CIDR ranges from a file.

    Arguments:
        file (str): Path to the input file.

    Returns:
        tuple: A tuple containing three lists: IP addresses, URLs, and CIDR ranges.
    """
    with open(file_name, encoding='utf-8') as targ_file:
        contents = targ_file.read()
    # Normalize contents (replace non-ASCII characters, trim whitespace)
    contents = "\n".join([punycode_domain(line.strip()) for line in contents.splitlines()])

    # Split lines and initialize lists
    lines = contents.split("\n")
    file_ip_addresses = set()
    file_cidr_ranges = set()
    file_urls = set()



    # Process each line
    for index, line in enumerate(lines, start=1):
        # Check for CIDR or IP ranges
        if re.match(IP_RANGE_REGEX, line):
            file_cidr_ranges.add(line)
        # Check for IPv4 and IPv6 addresses
        elif re.match(IP_REGEX, line) or re.match(IPV6_REGEX, line):
            file_ip_addresses.add(line)
        # Check for valid domains
        elif is_valid_domain(line):
            file_urls.add(line)
        else:
            print(f"Invalid record found in {file_name} at line {index}: {line}")

    return file_ip_addresses, file_urls, file_cidr_ranges

def write_to_file(data, filename):
    """
    Write data to a file.

    Arguments:
        data (list): A list of strings to be written to the file.
        filename (str): The name of the output file.
    """
    with open(filename, "w", encoding='utf-8') as outfile:
        outfile.write("\n".join(data))


if __name__ == "__main__":
    # Get a list of files matching the "targ-*" pattern in the current directory
    files = [f for f in os.listdir() if os.path.isfile(f) and f.startswith("targ-")]

    all_ip_addresses = []
    all_urls = []
    all_cidr_ranges = []

    # Loop through each file and extract IP addresses, URLs, and CIDR ranges
    for file in files:
        ip_addresses, urls, cidr_ranges = extract_data(file)
        all_ip_addresses.extend(ip_addresses)
        all_urls.extend(urls)
        all_cidr_ranges.extend(cidr_ranges)

    # Sort the data
    all_ip_addresses = sorted(set(all_ip_addresses))
    all_urls = sorted(set(all_urls))
    all_cidr_ranges = sorted(set(all_cidr_ranges))

    # Write the sorted data to separate output files
    if all_ip_addresses:
        write_to_file(all_ip_addresses, "sorted-ip.txt")
    if all_urls:
        write_to_file(all_urls, "sorted-url.txt")
    if all_cidr_ranges:
        write_to_file(all_cidr_ranges, "sorted-cidr.txt")

    # Write all the sorted data to a single output file
    all_sorted_data = all_ip_addresses + all_urls + all_cidr_ranges
    write_to_file(all_sorted_data, "sorted-all.txt")
