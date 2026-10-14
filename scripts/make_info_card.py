"""Step 4 - neofetch-style info card -> info-card.svg.  EDIT THE CONFIG BELOW."""
import os
from pathlib import Path
from xml.sax.saxutils import escape

HEADER = "nishant@github"
ROWS = [  # (key, value) - keep values short, the card is ~490px wide
    ("Name", "Nishant Parmar"),
    ("Now", "B.Tech CSE @ Parul University (2023-27)"),
    ("Prev", "Data Analyst Intern @ Bluestock Fintech"),
    ("Targets", "Full Stack Developer / Data Analyst"),
    ("Stack", "Python, SQL, Flask, MongoDB, Kotlin, Tableau"),
    ("Projects", "ResumeIQ, B100 Intelligence,"),
    ("", "Fresh-mart, SpendWise"),
    ("GitHub", "github.com/nishant9334"),
]
STATIC = os.environ.get("STATIC") == "1"

W, LINE, TOP = 490, 26, 78
H = TOP + len(ROWS) * LINE + 70
KEYCOL = "#58a6ff"
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
       f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
       "<style>.l{opacity:0;animation:in .45s ease-out forwards}"
       "@keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}"
       + (".l{opacity:1;animation:none}" if STATIC else "") + "</style>",
       f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>',
       f'<rect width="{W}" height="32" rx="10" fill="#161b22"/><rect y="20" width="{W}" height="12" fill="#161b22"/>',
       '<circle cx="18" cy="16" r="5" fill="#ff5f56"/><circle cx="36" cy="16" r="5" fill="#ffbd2e"/>'
       '<circle cx="54" cy="16" r="5" fill="#27c93f"/>',
       f'<text x="{W//2}" y="21" fill="#8b949e" font-size="12" text-anchor="middle">neofetch</text>']

def line(y, delay, inner):
    out.append(f'<g class="l" style="animation-delay:{delay:.2f}s">{inner}</g>')

line(TOP - 22, 0.2, f'<text x="24" y="{TOP-22}" fill="#39d353" font-size="16" font-weight="bold">{escape(HEADER)}</text>')
line(TOP - 8, 0.35, f'<text x="24" y="{TOP-8}" fill="#30363d" font-size="13">{"-" * 40}</text>')
for i, (k, v) in enumerate(ROWS):
    y = TOP + 16 + i * LINE
    key = f'<text x="24" y="{y}" fill="{KEYCOL}" font-size="14" font-weight="bold">{escape(k)}</text>' if k else ""
    val = f'<text x="110" y="{y}" fill="#c9d1d9" font-size="14">{escape(v)}</text>'
    line(y, 0.5 + i * 0.18, key + val)
# colour swatches like neofetch
sy = TOP + 16 + len(ROWS) * LINE + 14
sw = "".join(f'<rect x="{24 + n * 22}" y="{sy}" width="18" height="18" fill="{c}"/>'
             for n, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff", "#bc8cff", "#39c5cf", "#c9d1d9"]))
line(sy, 0.5 + len(ROWS) * 0.18 + 0.2, sw)
out.append("</svg>")

Path(__file__).resolve().parent.parent.joinpath("info-card.svg").write_text("\n".join(out))
print("Wrote info-card.svg")
