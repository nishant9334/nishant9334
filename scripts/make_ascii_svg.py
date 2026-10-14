"""Step 3b - source-prepped.png -> portrait-ascii.svg (self-typing monochrome ASCII)."""
from pathlib import Path
from xml.sax.saxutils import escape
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
RAMP = " .`:-=+*cs#%@"            # bright (sparse) -> dark (dense)
COLS, FS = 100, 7
CW, LH = FS * 0.6, FS * 1.0

img = Image.open(ROOT / "source-prepped.png").convert("L")
w, h = img.size
rows = max(1, int(h / w * COLS * 0.5))
a = np.asarray(img.resize((COLS, rows), Image.LANCZOS)) / 255.0
lines = ["".join(RAMP[min(len(RAMP) - 1, int((1 - v) * len(RAMP)))] for v in r).rstrip() for r in a]

W, H = COLS * CW, rows * LH + 8
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.1f} {H:.1f}">',
       "<defs>"]
for i in range(rows):
    out.append(f'<clipPath id="r{i}"><rect x="0" y="{i*LH:.1f}" height="{LH+1:.1f}" width="0">'
               f'<animate attributeName="width" from="0" to="{W:.1f}" begin="{i*0.05:.2f}s" dur="0.6s" fill="freeze"/>'
               f'</rect></clipPath>')
out.append("</defs>")
for i, s in enumerate(lines):
    if not s.strip():
        continue
    out.append(f'<g clip-path="url(#r{i})"><text xml:space="preserve" x="0" y="{(i+1)*LH:.1f}" font-size="{FS}" '
               f'font-family="ui-monospace,Menlo,Consolas,monospace" fill="#c9d1d9" '
               f'textLength="{len(s)*CW:.1f}" lengthAdjust="spacing">{escape(s)}</text></g>')
    out.append(f'<rect y="{i*LH:.1f}" width="{CW:.1f}" height="{LH:.1f}" fill="#39d353" opacity="0">'
               f'<animate attributeName="x" from="0" to="{W:.1f}" begin="{i*0.05:.2f}s" dur="0.6s" fill="freeze"/>'
               f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.02;0.98;1" begin="{i*0.05:.2f}s" dur="0.6s" fill="freeze"/></rect>')
out.append("</svg>")
(ROOT / "portrait-ascii.svg").write_text("\n".join(out))
print(f"Wrote portrait-ascii.svg ({COLS}x{rows} chars)")
