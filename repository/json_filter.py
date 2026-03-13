def filter_duplicate_elements(repo):

    pages = repo.get("pages", {})

    for page_name, elements in pages.items():

        seen = set()

        filtered = []

        for el in elements:

            key = (
                str(el.get("class")) +
                str(el.get("tag")) +
                str(el.get("id")) +
                str(el.get("type"))
            )

            if key in seen:
                continue

            seen.add(key)

            filtered.append(el)

        pages[page_name] = filtered

    return repo