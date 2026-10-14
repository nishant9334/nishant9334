"""Step 5b - draw contrib-heatmap.svg from data/contributions.json."""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "data" / "contributions.json").read_text())
days, st = data["days"], data["stats"]

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
CELL, GAP, LEFT, TOP = 13, 3, 36, 46
STEP = CELL + GAP
W = 860

counts = sorted(d["count"] for d in days if d["count"] > 0)
p95 = counts[int(len(counts) * 0.95)] if counts else 10**9

offset = (date.fromisoformat(days[0]["date"]).weekday() + 1) % 7  # Sunday-first rows
cols = (len(days) + offset - 1) // 7 + 1
H = TOP + 7 * STEP + 56

out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
       f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
       "<style>.c{opacity:0;animation:pop .5s ease-out forwards}"
       "@keyframes pop{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}"
       ".t{fill:#8b949e;font-size:11px}.s{fill:#c9d1d9;font-size:12px}</style>",
       f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117"/>']

# month labels
last_col, last_month = -9, None
for i, d in enumerate(days):
    m = d["date"][5:7]
    col = (i + offset) // 7
    if m != last_month and col - last_col >= 3:
        name = date.fromisoformat(d["date"]).strftime("%b")
        out.append(f'<text class="t" x="{LEFT + col * STEP}" y="{TOP - 10}">{name}</text>')
        last_col = col
    last_month = m

for r, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    out.append(f'<text class="t" x="8" y="{TOP + r * STEP + 11}">{label}</text>')

for i, d in enumerate(days):
    idx = i + offset
    col, row = idx // 7, idx % 7
    lvl = d["level"]
    if lvl >= 4 and d["count"] >= p95:
        lvl = 5
    delay = (col + row) * 0.012
    out.append(f'<rect class="c" style="animation-delay:{delay:.3f}s" x="{LEFT + col * STEP}" '
               f'y="{TOP + row * STEP}" width="{CELL}" height="{CELL}" rx="3" fill="{PALETTE[lvl]}"/>')

fy = TOP + 7 * STEP + 28
out.append(f'<text class="s" x="{LEFT}" y="{fy}">{st["total"]:,} contributions in the last year  |  '
           f'current streak {st["current_streak"]}d  |  longest {st["longest_streak"]}d</text>')
lx = W - 190
out.append(f'<text class="t" x="{lx}" y="{fy}">Less</text>')
for k, colr in enumerate(PALETTE):
    out.append(f'<rect x="{lx + 32 + k * 16}" y="{fy - 11}" width="{CELL}" height="{CELL}" rx="3" fill="{colr}"/>')
out.append(f'<text class="t" x="{lx + 32 + 6 * 16 + 4}" y="{fy}">More</text>')
out.append("</svg>")

(ROOT / "contrib-heatmap.svg").write_text("\n".join(out))
print("Wrote contrib-heatmap.svg")
