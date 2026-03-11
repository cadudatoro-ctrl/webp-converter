import os
import re

directory = '/Users/cadudatoro/0.works/CV/site provisorio/webp'
valid_exts = ('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff')
files = [f for f in os.listdir(directory) if f.lower().endswith(valid_exts)]
print(f"Total files matching exts: {len(files)}")

sequences_map = {}
pattern = re.compile(r'^(.*?)(\d+)\.[^.]+$')

for f in files:
    match = pattern.match(f)
    if match:
        prefix = match.group(1)
        seq_name = prefix if prefix else "Sequence (No Prefix)"
    else:
        seq_name = "Singles / Unsequenced"

    if seq_name not in sequences_map:
        sequences_map[seq_name] = []
    sequences_map[seq_name].append(f)

for seq, items in sequences_map.items():
    print(f"{seq}: {len(items)} items")

