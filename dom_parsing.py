import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from utils.object_repository import ObjectRepository

# ---------------- CONFIG ----------------
# URL = "https://my402955.s4hana.cloud.sap/ui#Shell-home"  # Replace with your SAP URL
URL = "https://my402955.s4hana.cloud.sap/ui#Shell-home"

OUTPUT_FOLDER = "object_repository"
SCREENSHOT_FOLDER = os.path.join(OUTPUT_FOLDER, "screenshots")
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
JSON_FILE = f"{OUTPUT_FOLDER}/object_repository.json"

# ---------------- SETUP ----------------
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(URL)
time.sleep(5)  # Better to use WebDriverWait in production

# Create folder if not exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

# ---------------- SMART XPATH ----------------
xpath_query = """
//input[not(@type='hidden')] |
 //button |
 //a |
 //select |
 //textarea |
 //*[@role='button'] |
 //*[@role='checkbox'] |
 //*[@role='radio']
"""

elements = driver.find_elements(By.XPATH, xpath_query)

object_repository = []

print(f"Total elements found (raw): {len(elements)}")

# ---------------- PROCESS ELEMENTS ----------------
for index, el in enumerate(elements):
    try:
        if not el.is_displayed():
            continue

        location = el.location
        size = el.size

        x = location['x']
        y = location['y']
        width = size['width']
        height = size['height']

        # Skip very small elements (icons < 5px etc.)
        if width < 5 or height < 5:
            continue

        element_name = f"{el.tag_name}_{index}"
        screenshot_path = os.path.join(SCREENSHOT_FOLDER, f"{element_name}.png")

        # Save element screenshot directly (better than manual cropping)
        el.screenshot(screenshot_path)

        element_data = {
            "element_name": element_name,
            "tag": el.tag_name,
            "text": el.text.strip(),
            "type": el.get_attribute("type"),
            "role": el.get_attribute("role"),
            "id": el.get_attribute("id"),
            "class": el.get_attribute("class"),
            "aria_label": el.get_attribute("aria-label"),
            "coordinates": {
                "x": x,
                "y": y,
                "width": width,
                "height": height
            },
            "screenshot_path": screenshot_path
        }

        object_repository.append(element_data)

        print(f"Saved: {element_name}")

    except Exception as e:
        print("Error processing element:", e)

# ---------------- SAVE JSON ----------------
with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(object_repository, f, indent=4)

print("Done. Object repository generated successfully.")
driver.quit()

# ---------------- CREATE UIPATH FORMAT ----------------
# Use ObjectRepository to build UiPath-style repository
app_name = "SAPApp"  # You can parameterize this
screen_name = "ShellHome"  # You can parameterize this
repo = ObjectRepository()
repo.add_application(app_name, version="1.0.0", app_type="Web")
repo.add_screen(app_name, screen_name, url=URL)

for el in object_repository:
    # Try to choose selector type and value
    selector = None
    selector_type = None
    if el["id"]:
        selector = el["id"]
        selector_type = "id"
    elif el["class"]:
        selector = el["class"]
        selector_type = "class"
    elif el["role"]:
        selector = el["role"]
        selector_type = "role"
    elif el["tag"]:
        selector = el["tag"]
        selector_type = "tag"
    else:
        selector = el["element_name"]
        selector_type = "name"
    # Element type: use tag/type/role
    element_type = el["type"] or el["tag"] or el["role"] or "Unknown"
    repo.add_element(app_name, screen_name, el["element_name"], selector, selector_type, element_type)

repo.save()
print("UiPath-style object repository saved as repository.json")
