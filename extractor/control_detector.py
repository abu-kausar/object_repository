def detect_control(tag, el_type, role, el):

    tag = (tag or "").lower()
    el_type = (el_type or "").lower()
    role = (role or "").lower()

    try:
        aria_checked = el.get_attribute("aria-checked")
        aria_selected = el.get_attribute("aria-selected")
        aria_expanded = el.get_attribute("aria-expanded")
        href = el.get_attribute("href")
        onclick = el.get_attribute("onclick")
        tabindex = el.get_attribute("tabindex")
    except:
        return "element"

    if tag == "input":

        if el_type in ["text", ""]:
            return "textbox"

        if el_type == "password":
            return "password"

        if el_type == "checkbox":
            return "checkbox"

        if el_type == "radio":
            return "radio"

        if el_type == "button":
            return "button"

    if tag == "button":
        return "button"

    if tag == "a":
        return "link"

    if role == "button":
        return "button"

    if aria_checked is not None:
        return "checkbox"

    if onclick:
        return "button"

    if tabindex is not None:
        return "focusable"

    return "element"