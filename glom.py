#!/usr/bin/python3

import os
import sys

def waltz(root):
    for root, _, files in os.walk(root):
        for f in files:
            p = os.path.join(root, f)
            stat = os.stat(p)
            if stat.st_size < 1000 and not os.environ.get("INCLUDE_SMOL"):
                continue
            yield((p, stat))


if len(sys.argv) < 3:
    sys.stderr.write("Builds an index from the files in primary_path to ")
    sys.stderr.write("find dupes in secondary_paths.\n")
    sys.stderr.write("Usage: ./glom.py primary_dir secondary_dir [...]\n")
    sys.exit(1)

primary = sys.argv[1]
secondaries = sys.argv[2:]

primary_files = {p: stat for p, stat in waltz(primary)}
by_size = {stat.st_size: (p, None) for p, stat in primary_files.items()}

print(primary_files)
print(by_size)
