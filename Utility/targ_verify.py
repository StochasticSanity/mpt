#!/usr/bin/env python

"""
Script Name: targ-verify.py
Author: Joseph Erdosy (@StochasticSanity)
Date: 01/09/2023

Description:
This script loops through all the files in the current directory (except for itself), 
removes leading/trailing whitespace, and validates each line to ensure it is a valid domain, 
subdomain, IP address, IP range, or CIDR block.
- If an invalid line is found, a warning message will be output to the console with the 
  file name and line number.
- If the line was modified (i.e. leading/trailing whitespace removed), it replaces the original line 
  with the modified line in the file.
- If no invalid lines are found, a message saying "All clear" will be output to the console.

Requirements:
- Python 3.6 or later
"""

import os
import re


def is_valid_line(line):
    """
    Checks if a line is a valid domain, subdomain, IP address, IP range, or CIDR block.

    Args:
    - line: A string containing the line to check.

    Returns:
    - True if the line is valid, False otherwise.
    """
    # Define regular expression patterns for each type of valid line
    domain_pattern = r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
    ip_address_pattern = r"^(?:(?:\d{1,3}\.){3}\d{1,3})(?:/(?:[1-9]|[1-2]\d|3[0-2]))?$"

    # Check if the line matches any of the patterns
    return bool(re.match(domain_pattern, line)) or bool(re.match(ip_address_pattern, line))


def verify_files():
    """
    Loops through all the files in the current directory (except for itself), removes 
    leading/trailing whitespace, and validates each line to ensure it is a valid domain, 
    subdomain, IP address, IP range, or CIDR block.
    - If an invalid line is found, a warning message will be output to the console with the file
      name and line number.
    - If the line was modified (i.e. leading/trailing whitespace removed), it replaces the original
      line with the modified line in the file.
    - If no invalid lines are found, a message saying "All clear" will be output to the console.
    """
    current_dir = os.getcwd()
    print(f"Current Directory: {current_dir}")

    invalid_found = False

    for file in os.listdir(current_dir):
        if file.endswith(".py"):
            continue

        file_path = os.path.join(current_dir, file)
        with open(file_path, "r+", encoding='utf-8') as targ_file:
            lines = targ_file.readlines()
            targ_file.seek(0)
            targ_file.truncate(0)

            for i, line in enumerate(lines, start=1):
                line = line.strip()
                if line != "" and not is_valid_line(line):
                    print(f"{file_path} ({i}): Invalid line: {line}")
                    invalid_found = True
                else:
                    targ_file.write(line + "\n")

            if invalid_found:
                print(
                    f"{file_path} has invalid lines, please fix them before proceeding.")
            else:
                print(f"{file_path} is clean.")

    if not invalid_found:
        print("All clear")


if __name__ == "__main__":
    verify_files()
