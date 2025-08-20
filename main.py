from PIL import Image
import os
import math
from collections import deque

SRC_DIR = "input"
DST_DIR = "out"
TARGET_HEX = "0b0d0d"
REPLACEMENT = (0, 0, 0, 0)
FUZZ = 0.08
TRIM_ALPHA_THRESHOLD = 1


def hex_to_rgb(s):
    s = s.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(ch*2 for ch in s)
    if len(s) not in (6, 8):
        raise ValueError(f"Bad hex '{s}'")
    r = int(s[0:2], 16)
    g = int(s[2:4], 16)
    b = int(s[4:6], 16)
    a = int(s[6:8], 16) if len(s) == 8 else 255
    return (r, g, b, a)


def close_enough_rgb(a, b, fuzz):
    dr, dg, db = a[0]-b[0], a[1]-b[1], a[2]-b[2]
    dist = math.sqrt(dr*dr + dg*dg + db*db)
    return (dist / (math.sqrt(3)*255)) <= fuzz


def is_target_pixel(px_val, target_rgba, fuzz):
    r, g, b, a = px_val
    if a <= TRIM_ALPHA_THRESHOLD:
        return False
    return close_enough_rgb((r, g, b, a), target_rgba, fuzz)


os.makedirs(DST_DIR, exist_ok=True)
TARGET = hex_to_rgb(TARGET_HEX)

for name in os.listdir(SRC_DIR):
    if not name.lower().endswith(".png"):
        continue

    src_path = os.path.join(SRC_DIR, name)
    im = Image.open(src_path).convert("RGBA")
    w, h = im.size
    px = im.load()

    visited = [[False]*w for _ in range(h)]
    q = deque()

    for x in range(w):
        q.append((x, 0))
        q.append((x, h-1))
    for y in range(h):
        q.append((0, y))
        q.append((w-1, y))

    while q:
        x, y = q.popleft()
        if visited[y][x]:
            continue
        visited[y][x] = True

        if is_target_pixel(px[x, y], TARGET, FUZZ):
            if len(REPLACEMENT) == 4:
                px[x, y] = REPLACEMENT
            else:
                r, g, b, a = px[x, y]
                px[x, y] = (*REPLACEMENT, a)

            if y > 0 and not visited[y-1][x]:
                q.append((x, y-1))
            if y < h-1 and not visited[y+1][x]:
                q.append((x, y+1))
            if x > 0 and not visited[y][x-1]:
                q.append((x-1, y))
            if x < w-1 and not visited[y][x+1]:
                q.append((x+1, y))

    alpha = im.getchannel("A")
    bin_mask = alpha.point(lambda v: 255 if v >
                           TRIM_ALPHA_THRESHOLD else 0, mode="1")
    bbox = bin_mask.getbbox()
    if bbox:
        im = im.crop(bbox)

    out_path = os.path.join(DST_DIR, name)
    im.save(out_path, optimize=True)
    print("Saved:", out_path)
