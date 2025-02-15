import re
import lib

hex_addresses = set()


def extract_hex_addresses(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Initialize variables to track the current state
    current_address = None

    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        if line.endswith(lib.GLOBAL_END_INDICATOR):
            if current_address:
                hex_addresses.add(current_address)
                current_address = None
        elif ":" in line:
            # Find the part before the colon
            part_before_colon = line.split(":")[0].strip()
            if all(c in "0123456789abcdefABCDEF" for c in part_before_colon):
                current_address = part_before_colon

    return hex_addresses


def extract_jump_instruction_addresses(jump_file_path):
    with open(jump_file_path, "r") as file:
        for line in file:
            line = line.strip()

            if line:
                hex_addresses.add(line)


def extract_hex_addresses_from_mid_instructions(mid_file_path):
    with open(mid_file_path, "r") as file:
        for line in file:
            line = line.strip()

            if line:
                hex_addresses.add(line)


file_path = "decompiled_code"
mid_file_path = "mid_addresses"
jump_file_path = "jump_instructions"
# extract_hex_addresses(file_path)
extract_hex_addresses_from_mid_instructions(mid_file_path)
original_hex_addresses_len = len(hex_addresses)
extract_jump_instruction_addresses(jump_file_path)
with open("addresses", "w") as file:
    for address in hex_addresses:
        file.write(address + "\n")
print("Amount of addresses:", -original_hex_addresses_len + len(hex_addresses))
