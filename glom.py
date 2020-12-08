#!/usr/bin/python3

import collections
import hashlib
import json
import os
import sys


ContentID = collections.namedtuple("ContentID", ["path", "size", "digest"])
block_size_mb = int(os.environ.get("BLOCK_SIZE_MB", 64))


def waltz(root):
    for root, _, files in os.walk(root):
        for f in files:
            p = os.path.join(root, f)
            stat = os.stat(p)
            if stat.st_size < 1000 and not os.environ.get("INCLUDE_SMOL"):
                continue
            yield((p, stat))

def hash_file(path):
    f = open(path, 'rb')
    hasher = hashlib.sha1()
    while True:
        block = f.read(block_size_mb*1000*1000)
        if not block:
            return hasher.hexdigest()
        hasher.update(block)


if len(sys.argv) < 3:
    sys.stderr.write("Builds an index from the files in primary_path to ")
    sys.stderr.write("find dupes in secondary_paths.\n")
    sys.stderr.write("Usage: ./glom.py primary_dir secondary_dir [...]\n")
    sys.exit(1)

primary = sys.argv[1]
secondaries = sys.argv[2:]

primary_files = {p: stat for p, stat in waltz(primary)}
primaries_by_size = {}
for p, stat in primary_files.items():
    size = stat.st_size
    have = primaries_by_size.get(size, [])
    primaries_by_size[size] = have + [ContentID(p, stat.st_size, None)]

secondary_files = {}
for s in secondaries:
    secondary_files.update({p: stat for p, stat in waltz(s)})

dupes = {}

for p, stat in secondary_files.items():
    size = stat.st_size
    pcids = primaries_by_size.get(size)
    if not pcids:
        # nothing matches this in our primaries
        continue
    for pcid in pcids:
        if not pcid.digest:
            new_pcid = ContentID(pcid.path, pcid.size, hash_file(pcid.path))
            primaries_by_size[size] = new_pcid
            pcid = new_pcid

        digest = hash_file(p)
        if digest != pcid.digest:
            continue

        if pcid.path in dupes:
            dupes[pcid.path]["matches"] += [p]
        else:
            dupes[pcid.path] = {"individual_size": size, "matches": [p]}

print(json.dumps(dupes, sort_keys=True, indent=4))
