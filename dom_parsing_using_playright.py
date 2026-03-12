from playwright.sync_api import sync_playwright, Error
import json
import os
import sys
from urllib.parse import urlparse
from PIL import Image, ImageDraw, ImageFont
import re

# -----------------------------
# Base name from URL
# -----------------------------
def get_base_name(url):

    parsed = urlparse(url)

    name = parsed.netloc.replace(":", "_")

    name = re.sub(r'[\\/*?:"<>|]', "_", name)

    return name


# -----------------------------
# Screen name from TAB TITLE
# -----------------------------
import re


def get_screen_name(page):

    try:

        title = page.title()

        if not title:
            title = "untitled"

        # remove invalid filename chars
        title = re.sub(r'[\\/*?:"<>|]', "_", title)

        # remove extra spaces
        title = title.strip()

        # limit length (important for Windows)
        title = title[:120]

        return title

    except:
        return "unknown_page"


# -----------------------------
# Save JSON
# -----------------------------
def save_repo(repo, base_name):

    os.makedirs("output", exist_ok=True)

    file_path = f"output/{base_name}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(repo, f, indent=4)

    print("Saved ->", file_path)


# -----------------------------
# Screenshot
# -----------------------------
def take_screenshot(page, base_name, screen_name):

    dir_path = f"output/screenshots/{base_name}"

    os.makedirs(dir_path, exist_ok=True)

    file_path = f"{dir_path}/{screen_name}.png"

    page.screenshot(path=file_path, full_page=True)

    print("Screenshot ->", file_path)

def draw_all_pages(repo, base_name):

    img_dir = f"output/screenshots/{base_name}"
    out_dir = f"{img_dir}/annotated"

    os.makedirs(out_dir, exist_ok=True)

    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()

    pages = repo["pages"]

    for page_name, elements in pages.items():

        img_path = f"{img_dir}/{page_name}.png"

        if not os.path.exists(img_path):
            continue

        out_path = f"{out_dir}/{page_name}_anchor.png"

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

            t = el.get("control_type")

            color = "red"

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

        print("Annotated ->", out_path)




def get_control_type(el, tag, el_type, el_role, el_class, aria_checked):

    # 1. Real input tag 
    if tag == "input":
        if el_type == "checkbox":   return "checkbox"
        if el_type == "radio":      return "radio"
        if el_type == "password":   return "password"
        if el_type in ("text", "email", "search",
                       "tel", "url", "number", None):
                                    return "textbox"
        return el_type or "input"

    # 2. Textarea 
    if tag == "textarea":           return "textbox"

    # 3. Select
    if tag == "select":             return "select"

    # 4. ARIA roles (works for ANY framework) 
    if el_role == "checkbox" or aria_checked is not None:
                                    return "checkbox"
    if el_role == "radio":          return "radio"
    if el_role == "button":         return "button"

    #  5. Label/div/span wrapping a hidden input
    #    Works for SAP, Angular, Bootstrap, ANY framework
    if tag in ("label", "div", "span"):
        inner_checkbox = el.query_selector("input[type='checkbox']")
        if inner_checkbox:          return "checkbox"

        inner_radio = el.query_selector("input[type='radio']")
        if inner_radio:             return "radio"

    # 6. Native tags 
    if tag == "button":             return "button"
    if tag == "a":                  return "link"
    if tag == "label":              return "label"

    # 7. Fallback
    return tag
# -----------------------------
# Extract elements
# -----------------------------
def extract_elements(page, screen_name, repo):

    selectors = [
        "input:not([type='hidden'])",
        "input[type='checkbox']",
        "input[type='radio']",
        "button",
        "a",
        "select",
        "textarea",
        "label",
        "[role='button']",
        "[role='checkbox']",
        "[role='radio']",
        "[aria-checked]",
    ]

    if screen_name not in repo["pages"]:
        repo["pages"][screen_name] = []

    elements = []

    # keep selector with element
    for s in selectors:
        found = page.query_selector_all(s)

        for el in found:
            elements.append((el, s))

    print(f"[{screen_name}] Found {len(elements)}")

    for idx, (el, sel) in enumerate(elements):

        try:

            box = el.bounding_box()

            if not box:
                continue

            if box["width"] < 5 or box["height"] < 5:
                continue

            tag = el.evaluate(
                "e => e.tagName.toLowerCase()"
            )

            el_type = el.get_attribute("type")

            text = ""

            if tag not in ["input"]:
                text = el.inner_text()

            else:
                text = el.get_attribute("value")

            # el_info = {
            #     "name": f"{tag}_{idx}",
            #     "tag": tag,
            #     "text": text,
            #     "type": el_type,
            #     "id": el.get_attribute("id"),
            #     "class": el.get_attribute("class"),
            #     "role": el.get_attribute("role"),
            #     "aria_label": el.get_attribute("aria-label"),
            #     "selector": sel,
            #     "box": box,
            # }

            el_class     = el.get_attribute("class") or ""
            el_role      = el.get_attribute("role")  or ""
            aria_checked = el.get_attribute("aria-checked")

            # if tag == "input":
            #     if el_type == "checkbox":            control_type = "checkbox"
            #     elif el_type == "radio":             control_type = "radio"
            #     elif el_type == "password":          control_type = "password"
            #     elif el_type in ("text","email","search","tel","url","number",None):
            #                                         control_type = "textbox"
            #     else:                                control_type = el_type or "input"
            # elif tag == "textarea":                  control_type = "textbox"
            # elif tag == "select":                    control_type = "select"
            # elif tag == "button" or el_role == "button":
            #                                         control_type = "button"
            # elif el_role == "checkbox" or aria_checked is not None:
            #                                         control_type = "checkbox"
            # elif el_role == "radio":                 control_type = "radio"
            # # label/div/span acting as checkbox via CSS class (SAP Fiori pattern)
            # elif any(kw in el_class for kw in ("checkbox", "check-box", "fn-checkbox")):
            #                                         control_type = "checkbox"
            # elif any(kw in el_class for kw in ("radio", "radio-button")):
            #                                         control_type = "radio"
            # elif tag == "a":                         control_type = "link"
            # elif tag == "label":                     control_type = "label"
            # else:                                    control_type = tag
            # ────────────────────────────────────────────────────────────────

            control_type = get_control_type(
                el, tag, el_type, el_role, el_class, aria_checked
            )

            el_info = {
                "name": f"{tag}_{idx}",
                "tag": tag,
                "text": text,
                "type": el_type,
                "control_type": control_type,          # new field
                "id": el.get_attribute("id"),
                "class": el_class,
                "role": el_role or None,
                "aria_label": el.get_attribute("aria-label"),
                "selector": sel,
                "box": box,
            }

            # avoid duplicate
            if el_info not in repo["pages"][screen_name]:
                repo["pages"][screen_name].append(
                    el_info
                )

        except Exception:
            pass


# -----------------------------
# Main
# -----------------------------
def main():

    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "python script.py <url> [browser]"
        )
        sys.exit(1)

    url = sys.argv[1]

    browser_name = (
        sys.argv[2] if len(sys.argv) > 2 else "chromium"
    )

    base_name = get_base_name(url)

    repo = {
        "base_url": url,
        "pages": {}
    }

    try:

        with sync_playwright() as p:

            browser_type = getattr(
                p,
                browser_name
            )

            browser = browser_type.launch(
                headless=False
            )

            context = browser.new_context()

            page = context.new_page()

            # -------------------------
            # Navigation handler
            # -------------------------
            def on_nav(frame):

                if frame != page.main_frame:
                    return

                try:

                    page.wait_for_load_state(
                        "load"
                    )

                    screen_name = get_screen_name(
                        page
                    )

                    print(
                        "Navigated ->",
                        screen_name
                    )

                    extract_elements(
                        page,
                        screen_name,
                        repo
                    )

                    take_screenshot(
                        page,
                        base_name,
                        screen_name
                    )

                    save_repo(
                        repo,
                        base_name
                    )

                except Error:
                    pass


            page.on(
                "framenavigated",
                on_nav
            )

            # -------------------------
            # Close handler
            # -------------------------
            def on_close():

                print("Browser closed")

                save_repo(
                    repo,
                    base_name
                )

                draw_all_pages(
                    repo,
                    base_name
                )


            context.on(
                "close",
                lambda _: on_close()
            )

            # -------------------------
            # Start
            # -------------------------
            page.goto(url)

            print(
                "Running... close browser to stop"
            )

            page.wait_for_timeout(
                999999999
            )

    except Error:

        save_repo(
            repo,
            base_name
        )

        draw_all_pages(
            repo,
            base_name
        )

        print("Stopped safely")


if __name__ == "__main__":
    main()