from PIL import Image, ImageDraw, ImageFont
import os

input_dir = "input"
os.makedirs(input_dir, exist_ok=True)

# Generate 5 test images
colors = ['red', 'green', 'blue', 'yellow', 'cyan']

for i, color in enumerate(colors):
    img = Image.new('RGB', (800, 600), color=color)
    d = ImageDraw.Draw(img)
    # Just draw some text or shape
    d.text((380, 280), f"Frame {i+1}", fill=(0,0,0))
    img.save(f"{input_dir}/frame_{i+1:02d}.jpg")

print(f"Generated {len(colors)} images in {input_dir}/")
