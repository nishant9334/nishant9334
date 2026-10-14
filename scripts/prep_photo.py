"""Step 3a - prep a photo for ASCII conversion -> source-prepped.png.
Usage: python scripts/prep_photo.py my-photo.jpg
"""
import sys
import numpy as np
import cv2
from PIL import Image

if len(sys.argv) < 2:
    sys.exit("Usage: python scripts/prep_photo.py <photo>")

img = Image.open(sys.argv[1]).convert("RGBA")
try:
    from rembg import remove          # 1. remove background
    img = remove(img).convert("RGBA")
except ImportError:
    print("rembg not installed - background will NOT be removed (use a plain background photo).")

rgba = np.array(img)
alpha = rgba[..., 3] / 255.0
gray = cv2.cvtColor(rgba[..., :3], cv2.COLOR_RGB2GRAY)
gray = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)   # 2. local contrast
out = (gray * alpha + 255 * (1 - alpha)).astype(np.uint8)                # 3. composite on white
Image.fromarray(out).save("source-prepped.png")
print("Wrote source-prepped.png")
