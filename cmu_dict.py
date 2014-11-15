from collections import defaultdict
import re


def parse_cmudict(path):
    start_letter = re.compile("^\w")
    endings = defaultdict(list)
    with open(path) as f:
        for line in f:
            if start_letter.match(line):
                parts = line.strip().split(" ")
                endings["".join(parts[3:])].append(parts[0])
    return endings
