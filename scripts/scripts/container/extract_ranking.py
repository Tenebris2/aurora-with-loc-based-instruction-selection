import re
import sys
import pprint
from collections import defaultdict

args = sys.argv


def extract_after_at(arr):
    for i in range(len(arr)):
        if arr[i] == "at":
            return arr[i + 1]

    return "\n"


def extract_ranking(path, target):

    data = []

    temporary_data = set()
    with open(path, "r") as file:
        data = [extract_after_at(x.split(" ")).strip() for x in file.readlines()]
        count = 0
        for line in data:
            count += 1
            if line == target:
                break
            if ".c" in line or ".h" in line:
                temporary_data.add(line)

        data = temporary_data
        # pprint.pprint(temporary_data)
        print(f"Line ranking at: {len(data) + 1}")

        line_rank = len(data) + 1
        predicate_rank = count
        return predicate_rank, line_rank


def map_ranking(path, target):
    data = []

    temporary_data = defaultdict(int)
    with open(path, "r") as file:
        data = [extract_after_at(x.split(" ")).strip() for x in file.readlines()]
        count = 0
        for line in data:
            count += 1
            if line == target:
                break
            if ".c" in line or ".h" in line:
                temporary_data[line] += 1

        data = temporary_data
        # pprint.pprint(temporary_data)
        pprint.pprint(temporary_data)
