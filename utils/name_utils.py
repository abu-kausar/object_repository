import re
from urllib.parse import urlparse


def get_base_name(url):

    parsed = urlparse(url)

    name = parsed.netloc.replace(":", "_")

    name = re.sub(r'[\\/*?:"<>|]', "_", name)

    return name


def get_screen_name(page):

    try:

        title = page.title()

        if not title:
            title = "untitled"

        title = re.sub(r'[\\/*?:"<>|]', "_", title)

        return title.strip()[:120]

    except:
        return "unknown_page"