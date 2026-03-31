from extractor.control_detector import detect_control
from extractor.label_utils import get_label_text


class ElementExtractor:

    def __init__(self, repo):
        self.repo = repo

    def extract(self, page, screen_name):

        selectors = [

            "input:not([type='hidden'])",
            "textarea",
            "select",
            "button",
            "a",
            "label",

            "[role='button']",
            "[role='checkbox']",
            "[role='radio']",
            "[role='textbox']",
            "[role='combobox']",
            "[role='switch']",

            "[aria-label]",
            "[aria-checked]",
            "[aria-selected]",

            "[tabindex]",

            "[data-testid]",
            "[data-id]",
        ]

        if screen_name not in self.repo["pages"]:
            self.repo["pages"][screen_name] = []

        elements = []

        for s in selectors:

            for el in page.query_selector_all(s):
                elements.append((el, s))

        print(f"[{screen_name}] Found {len(elements)}")

        for idx, (el, sel) in enumerate(elements):

            try:

                box = el.bounding_box()

                if not box:
                    continue

                # if box["width"] < 5 or box["height"] < 5:
                #     continue

                tag = el.evaluate(
                    "e => e.tagName.toLowerCase()"
                )

                el_type = el.get_attribute("type")
                role = el.get_attribute("role")

                text = None

                if tag != "input":
                    text = el.inner_text()
                else:
                    text = el.get_attribute("value")

                el_id = el.get_attribute("id")

                name_attr = el.get_attribute("name")

                placeholder = el.get_attribute("placeholder")

                autocomplete = el.get_attribute("autocomplete")

                title = el.get_attribute("title")

                aria_label = el.get_attribute("aria-label")

                el_class = el.get_attribute("class")

                data_testid = el.get_attribute("data-testid")

                data_id = el.get_attribute("data-id")

                label = get_label_text(el)

                control_type = detect_control(
                    tag,
                    el_type,
                    role,
                    el
                )

                info = {

                    "name": f"{tag}_{idx}",

                    "control_type": control_type,

                    "tag": tag,

                    "text": text,

                    "type": el_type,

                    "id": el_id,

                    "name_attr": name_attr,

                    "placeholder": placeholder,

                    "autocomplete": autocomplete,

                    "title": title,

                    "label": label,

                    "class": el_class,

                    "role": role,

                    "aria_label": aria_label,

                    "data_testid": data_testid,

                    "data_id": data_id,

                    # "selector": sel, # previous, valid css selector
                    
                    "selector": ElementExtractor.normalize_selector(sel), # new although it is not a valid CSS selector, it is more consistent and easier to parse

                    "box": box,
                }

                if info not in self.repo["pages"][screen_name]:
                    self.repo["pages"][screen_name].append(info)

            except:
                pass
    
    @staticmethod
    def normalize_selector(sel: str) -> str:

        # case 1: convert :not([type='hidden'])
        if sel.startswith("input:not("):
            inner = sel.replace("input:not(", "").rstrip(")")
            
            # OPTION A (your requested format)
            return f"input({inner})"

            # OPTION B (recommended valid CSS)
            # return f"input{inner}"

        return sel