"""
Generate a file with IP addresses.

    Args:
        --output-file: The filename to be used for output. 

"""

import argparse

IP_RANGES = {
    "first_octet_range": (10, 10, 1),
    "second_octet_range": (0, 255, 1),
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
        for first_octet in range(*first_octet_range):
            for second_octet in range(*second_octet_range):
                for third_octet in range(*third_octet_range):
                    for fourth_octet in range(*fourth_octet_range):
                        ip_addr = [str(first_octet), str(second_octet),
                                   str(third_octet), str(fourth_octet)]
                        ip_curr = ".".join(ip_addr)
                        output.write(ip_curr + "\n")
                        count += 1

    print(f"Printed {count} IPs to file {output_file}!")


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate a file with IP addresses")
    parser.add_argument("--output-file", "-o",
                        default="gen-output.txt",
                        help="Name and path of output file")
    args = parser.parse_args()

    # Generate the IP addresses and write them to the output file
    generate_ips(**IP_RANGES, output_file=args.output_file)
