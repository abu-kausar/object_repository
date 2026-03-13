import os
from PIL import Image, ImageDraw, ImageFont


class DrawAnnotator:

    def __init__(self, base_name, repo):

        self.base_name = base_name
        self.repo = repo

        self.img_dir = f"output/screenshots/{base_name}"
        self.out_dir = f"{self.img_dir}/annotated"

        os.makedirs(self.out_dir, exist_ok=True)

        try:
            self.font = ImageFont.truetype(
                "arial.ttf",
                14
            )
        except:
            self.font = ImageFont.load_default()

    # -------------------------
    # color by control type
    # -------------------------
    def get_color(self, t):

        if t == "textbox":
            return "blue"

        if t == "password":
            return "purple"

        if t == "button":
            return "green"

        if t == "checkbox":
            return "orange"

        if t == "radio":
            return "yellow"

        if t == "link":
            return "cyan"

        if t == "dropdown":
            return "pink"

        return "red"

    # -------------------------
    # draw single page
    # -------------------------
    def draw_page(self, page_name, elements):

        img_path = f"{self.img_dir}/{page_name}.png"

        if not os.path.exists(img_path):
            return

        out_path = f"{self.out_dir}/{page_name}_anchor.png"

        img = Image.open(img_path)

        draw = ImageDraw.Draw(img)

        for el in elements:

            box = el.get("box")

            if not box:
                continue

            x = box["x"]
            y = box["y"]
            w = box["width"]
            h = box["height"]

            x2 = x + w
            y2 = y + h

            t = el.get("control_type")

            color = self.get_color(t)

            # draw rectangle
            draw.rectangle(
                [x, y, x2, y2],
                outline=color,
                width=2
            )

            # label text
            label = el.get("name", "")

            if el.get("id"):
                label += f" | {el['id']}"

            if t:
                label += f" | {t}"

            # label bg
            draw.rectangle(
                [x, y - 15, x + 240, y],
                fill=color
            )

            draw.text(
                (x + 2, y - 14),
                label,
                fill="white",
                font=self.font
            )

        img.save(out_path)

        print("Annotated ->", out_path)

    # -------------------------
    # draw all pages
    # -------------------------
    def draw_all(self):

        pages = self.repo.get("pages", {})

        for page_name, elements in pages.items():

            self.draw_page(
                page_name,
                elements
            )