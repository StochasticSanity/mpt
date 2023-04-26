"""
Generate a file with IP addresses.

    Args:
        --output-file: The filename to be used for output. 

"""

import argparse
import itertools
import sys

IP_RANGES = {
    "first_octet_range": (192, 192, 1),
    "second_octet_range": (168, 168, 1),
    "third_octet_range": (0, 255, 1),
    "fourth_octet_range": (1, 1, 1)
}


def generate_ips(first_octet_range, second_octet_range, third_octet_range, fourth_octet_range,
                 output_file):
    """
    Generate a file with IP addresses.

    Args:
        first_octet_range (tuple): Range for the first octet of the IP address.
        second_octet_range (tuple): Range for the second octet of the IP address.
        third_octet_range (tuple): Range for the third octet of the IP address.
        fourth_octet_range (tuple): Range for the fourth octet of the IP address.
        output_file (str): Name and path of output file.
    """
    count = 0
    with open(output_file, "a", encoding="utf-8") as output:
        for ip_addr in itertools.product(
                range(first_octet_range[0], first_octet_range[1] + 1, first_octet_range[2]),
                range(second_octet_range[0], second_octet_range[1] + 1, second_octet_range[2]),
                range(third_octet_range[0], third_octet_range[1] + 1, third_octet_range[2]),
                range(fourth_octet_range[0], fourth_octet_range[1] + 1, fourth_octet_range[2])):
            ip_curr = ".".join(map(str, ip_addr))
            output.write(ip_curr + "\n")
            count += 1

    print(f"Printed {count} IPs to file {output_file}!")


def validate_ranges(ip_ranges):
    """
    Validate the IP ranges provided by the user.

    Args:
        ip_ranges (dict): A dictionary containing the IP ranges for each octet.

    Raises:
        ValueError: If the IP ranges are invalid or would generate invalid IP addresses.
    """
    for octet_name, octet_range in ip_ranges.items():
        start, end, step = octet_range
        if start > end or start < 0 or end > 255 or step <= 0:
            raise ValueError(f"Invalid range for {octet_name}: {octet_range}")

    # Check for invalid first octet values
    first_start, first_end, _ = ip_ranges["first_octet_range"]
    if first_start == 0 or first_start == 127 or 224 <= first_start <= 239:
        raise ValueError(f"Invalid starting value for first_octet_range: {first_start}")
    if first_end == 0 or first_end == 127 or 224 <= first_end <= 239:
        raise ValueError(f"Invalid ending value for first_octet_range: {first_end}")

    # Check for invalid fourth octet values
    fourth_start, fourth_end, _ = ip_ranges["fourth_octet_range"]
    if fourth_start == 255:
        raise ValueError(f"Invalid starting value for fourth_octet_range: {fourth_start}")
    if fourth_end == 255:
        raise ValueError(f"Invalid ending value for fourth_octet_range: {fourth_end}")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate a file with IP addresses")
    parser.add_argument("--output-file", "-o",
                        default="gen-output.txt",
                        help="Name and path of output file")
    args = parser.parse_args()

    try:
        validate_ranges(IP_RANGES)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Generate the IP addresses and write them to the output file
    generate_ips(**IP_RANGES, output_file=args.output_file)
