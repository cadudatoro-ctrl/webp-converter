import os
from PIL import Image

input_dir = "input"
output_file = "output/test_anim.webp"
os.makedirs("output", exist_ok=True)

files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
files.sort()

frames = []
for f in files:
    path = os.path.join(input_dir, f)
    img = Image.open(path)
    frames.append(img)

# Save test with 10 fps (100ms)
frames[0].save(
    output_file,
    format="WebP",
    save_all=True,
    append_images=frames[1:],
    duration=100,
    loop=0,
    quality=80
)

print(f"Saved to {output_file}")
# Verify the saved file
saved = Image.open(output_file)
frames_count = saved.n_frames
print(f"Verification: output file has {frames_count} frames, format is {saved.format}")
