import json
from datetime import datetime

INPUT = "data/contributions.json"
OUTPUT = "contrib-heatmap.svg"

PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0",
]

with open(INPUT) as f:
    data = json.load(f)

days = data["days"]

# Keep the most recent 371 days (53 weeks)
days = days[-371:]

while len(days) < 371:
    days.insert(0, {"date": "", "level": 0})

cell = 12
gap = 3
step = cell + gap

left = 35
top = 25
width = left + 53 * step + 20
height = top + 7 * step + 55

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{width}" height="{height}" '
    f'viewBox="0 0 {width} {height}">',
    '<rect width="100%" height="100%" fill="#0d1117"/>',
]

# Draw cells
for i, day in enumerate(days):
    week = i // 7
    weekday = i % 7

    x = left + week * step
    y = top + weekday * step
    level = max(0, min(5, day["level"]))

    delay = (week + weekday) * 0.025

    svg.append(
        f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
        f'rx="3" fill="{PALETTE[level]}" opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" '
        f'begin="{delay:.3f}s" dur="0.3s" fill="freeze"/>'
        f'</rect>'
    )

# Legend
legend_y = top + 7 * step + 20

svg.append(
    f'<text x="{left}" y="{legend_y}" fill="#8b949e" '
    f'font-family="monospace" font-size="11">Less</text>'
)

for i in range(6):
    x = left + 35 + i * 16

    svg.append(
        f'<rect x="{x}" y="{legend_y - 10}" width="12" height="12" '
        f'rx="3" fill="{PALETTE[i]}"/>'
    )

svg.append(
    f'<text x="{left + 135}" y="{legend_y}" fill="#8b949e" '
    f'font-family="monospace" font-size="11">More</text>'
)

svg.append(
    f'<text x="{left}" y="{height - 8}" fill="#8b949e" '
    f'font-family="monospace" font-size="11">'
    f'GitHub contributions — {data["username"]}'
    f'</text>'
)

svg.append("</svg>")

with open(OUTPUT, "w") as f:
    f.write("\n".join(svg))

print(f"Created {OUTPUT}")