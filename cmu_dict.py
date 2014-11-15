import re


def parse_cmudict(path):
    start_letter = re.compile("^\w")
    with open(path) as f:
        for line in f:
            if start_letter.match(line):
                parts = line.strip().split(" ")
                yield (parts[0], parts[-1])
