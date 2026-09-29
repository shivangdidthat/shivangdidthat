from rembg import remove
from PIL import Image
import cv2
import numpy as np

input_file = "source-photo.jpg"
output_file = "source-prepped.png"

# Remove background
with open(input_file, "rb") as f:
    input_data = f.read()

output_data = remove(input_data)

with open("temp.png", "wb") as f:
    f.write(output_data)

# Open image
img = Image.open("temp.png").convert("RGBA")

# White background
background = Image.new("RGBA", img.size, "white")
background.alpha_composite(img)
gray = background.convert("L")

# Improve local contrast
arr = np.array(gray)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
arr = clahe.apply(arr)

Image.fromarray(arr).save(output_file)

print(f"Created {output_file}")