from PIL import Image

INPUT = "source-prepped.png"
OUTPUT = "avi-ascii.svg"

RAMP = " .`:-=+*cs#%@"
WIDTH = 100

img = Image.open(INPUT).convert("L")

# Character cells are taller than they are wide.
char_ratio = 0.5
height = int(img.height / img.width * WIDTH * char_ratio)
img = img.resize((WIDTH, height))

pixels = img.load()

rows = []

for y in range(height):
    row = []
    for x in range(WIDTH):
        brightness = pixels[x, y]
        index = int((255 - brightness) / 256 * len(RAMP))
        index = min(index, len(RAMP) - 1)
        row.append(RAMP[index])
    rows.append("".join(row))

line_height = 10
svg_width = WIDTH * 7
svg_height = height * line_height

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{svg_width}" height="{svg_height}" '
    f'viewBox="0 0 {svg_width} {svg_height}">',
    '<rect width="100%" height="100%" fill="white"/>',
    '<style>',
    '.ascii { font-family: monospace; font-size: 10px; fill: #555; }',
    '</style>'
]

for y, row in enumerate(rows):
    escaped = (
        row.replace("&", "&amp;")
           .replace("<", "&lt;")
           .replace(">", "&gt;")
    )

    svg.append(
        f'<text x="0" y="{(y + 1) * line_height}" '
        f'class="ascii" opacity="0">'
        f'{escaped}'
        f'<animate attributeName="opacity" '
        f'from="0" to="1" begin="{y * 0.04}s" '
        f'dur="0.15s" fill="freeze"/>'
        f'</text>'
    )

svg.append("</svg>")

with open(OUTPUT, "w") as f:
    f.write("\n".join(svg))

print(f"Created {OUTPUT}")