import os

OUTPUT = "info-card.svg"
STATIC = os.getenv("STATIC") == "1"

lines = [
    ("Now", "Building my GitHub profile"),
    ("Prev", "Learning & creating"),
    ("Stack", "Python • Git • GitHub"),
    ("Focus", "Data • Analytics • Tech"),
]

width = 490
height = 250

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
    '<rect width="100%" height="100%" rx="14" fill="#0d1117" stroke="#30363d"/>',
    '<text x="24" y="35" fill="#58a6ff" font-family="monospace" font-size="16" font-weight="bold">shivang@github ~</text>',
]

for i, (key, value) in enumerate(lines):
    y = 75 + i * 40
    delay = i * 0.25

    if STATIC:
        opacity = '1'
        animation = ''
    else:
        opacity = '0'
        animation = (
            f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{delay}s" dur="0.4s" fill="freeze"/>'
        )

    svg.append(
        f'<text x="24" y="{y}" fill="#8b949e" '
        f'font-family="monospace" font-size="14" opacity="{opacity}">'
        f'<tspan fill="#79c0ff">{key:10}</tspan>'
        f'<tspan fill="#c9d1d9"> {value}</tspan>'
        f'{animation}</text>'
    )

svg.append("</svg>")

with open(OUTPUT, "w") as f:
    f.write("\n".join(svg))

print(f"Created {OUTPUT}")