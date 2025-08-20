from PIL import Image
import os

SRC_DIR = "out"
DST_DIR = "out2"
FILL_COLOR = (0x21, 0x22, 0x22, 255)

os.makedirs(DST_DIR, exist_ok=True)

for name in os.listdir(SRC_DIR):
    if not name.lower().endswith(".png"):
        continue

    src_path = os.path.join(SRC_DIR, name)
    im = Image.open(src_path).convert("RGBA")
    w, h = im.size
    px = im.load()

    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 255:
                px[x, y] = FILL_COLOR

    out_path = os.path.join(DST_DIR, name)
    im.save(out_path, optimize=True)
    print("Saved:", out_path)
