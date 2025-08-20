from PIL import Image
import os

SRC_DIR = "input"
DST_DIR = "input"
FILENAME = "plugin-pinger.png"

os.makedirs(DST_DIR, exist_ok=True)

src_path = os.path.join(SRC_DIR, FILENAME)
im = Image.open(src_path)

w, h = im.size
im_cropped = im.crop((0, 0, w-1, h))

out_path = os.path.join(DST_DIR, FILENAME)
im_cropped.save(out_path, optimize=True)
print("Saved:", out_path)
