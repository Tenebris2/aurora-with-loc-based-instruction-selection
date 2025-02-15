import sys
import re
from enum import Enum


class SelectionMethod(Enum):
    BEGIN = 1
    MIDDLE = 2
    END = 3


#
# def extract_addresses(filepath, outpath):
#     addresses = []
#     with open(filepath, "r") as file:
#         lines = file.readlines()
#
#     for i in range(1, len(lines)):
#         if "/home/" in lines[i] or "/Aurora/" in lines[i]:
#             # Extract the address from the line before
#             match = re.search(r"([0-9a-fA-F]+):", lines[i - 1])
#             if match:
#                 addresses.append(match.group(1))
#
#     with open(outpath, "w") as outfile:
#         for address in addresses:
#             outfile.write(address + "\n")


def extract_addresses(filepath, outpath, selection_method):
    addresses = []
    addr = []
    with open(filepath, "r") as file:
        lines = file.readlines()
    begin = False
    for i in range(1, len(lines) - 1):
        if begin == True:
            match = re.search(r"([0-9a-fA-F]+):", lines[i])
            if match:
                addr.append(match.group(1))

        if (
            "/home/" in lines[i + 1]
            or "/Aurora/" in lines[i + 1]
            or "/evaluation" in lines[i + 1]
        ):
            begin = True
            addr = addr[1:]
            if len(addr) >= 1:
                if selection_method == SelectionMethod.BEGIN:
                    addresses.append(addr[0])
                elif selection_method == SelectionMethod.MIDDLE:
                    addresses.append(addr[len(addr) // 2])
                elif selection_method == SelectionMethod.END:
                    addresses.append(addr[len(addr) - 1])
            else:
                continue
            addr = []
            # Extract the address from the line before
    with open(outpath, "w") as outfile:
        for address in addresses:
            outfile.write(address + "\n")


# Example usage
filepath = sys.argv[1]
outpath = "addresses"
addresses = extract_addresses(filepath, outpath, SelectionMethod.BEGIN)
