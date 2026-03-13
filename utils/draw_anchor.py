import json
import os
from PIL import Image, ImageDraw, ImageFont


# -------------------------
# CHANGE THIS ONLY
# -------------------------

BASE_NAME = "your_site.com"


# -------------------------
# Paths
# -------------------------

JSON_PATH = f"output/{BASE_NAME}.json"

IMG_DIR = f"output/screenshots/{BASE_NAME}"

OUT_DIR = f"{IMG_DIR}/annotated"

os.makedirs(OUT_DIR, exist_ok=True)


# -------------------------
# Load repo
# -------------------------

with open(JSON_PATH, "r", encoding="utf-8") as f:
    repo = json.load(f)


pages = repo["pages"]


# -------------------------
# Font
# -------------------------

try:
    font = ImageFont.truetype("arial.ttf", 14)
except:
    font = ImageFont.load_default()


# -------------------------
# Draw function
# -------------------------

def draw_page(page_name, elements):

    img_path = f"{IMG_DIR}/{page_name}.png"

    if not os.path.exists(img_path):
        print("Missing screenshot:", page_name)
        return

    out_path = f"{OUT_DIR}/{page_name}_anchor.png"

    img = Image.open(img_path)

    draw = ImageDraw.Draw(img)

    for el in elements:

        box = el["box"]

        x = box["x"]
        y = box["y"]
        w = box["width"]
        h = box["height"]

        x2 = x + w
        y2 = y + h

        # color by type
        color = "red"

        t = el.get("control_type")

        if t == "textbox":
            color = "blue"

        elif t == "password":
            color = "purple"

        elif t == "button":
            color = "green"

        elif t == "checkbox":
            color = "orange"

        elif t == "radio":
            color = "yellow"

        # box
        draw.rectangle(
            [x, y, x2, y2],
            outline=color,
            width=2
        )

        label = el["name"]

        if el.get("id"):
            label += f" | {el['id']}"

        if t:
            label += f" | {t}"

        # label background
        draw.rectangle(
            [x, y - 15, x + 220, y],
            fill=color
        )

        draw.text(
            (x + 2, y - 14),
            label,
            fill="white",
            font=font
        )

    img.save(out_path)

    print("Saved ->", out_path)


# -------------------------
# Loop all pages
# -------------------------

for page_name, elements in pages.items():

    draw_page(page_name, elements)