import os
from PIL import Image

input_dir = "input"
os.makedirs(input_dir, exist_ok=True)

sequences = {
    "walk_": 5,
    "run_": 3,
    "idle": 4  # e.g., idle01, idle02
}

for prefix, count in sequences.items():
    for i in range(count):
        img = Image.new('RGB', (100, 100), color='white')
        # format name based on prefix
        if prefix.endswith("_"):
            filename = f"{prefix}{i+1:03d}.png"
        else:
            filename = f"{prefix}{i+1:02d}.jpg"
            
        img.save(os.path.join(input_dir, filename))

# Add a single file to test "unsequenced" bucket
img = Image.new('RGB', (100, 100), color='black')
img.save(os.path.join(input_dir, "background.png"))

print("Generated dummy multi-sequence files.")
