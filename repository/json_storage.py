import json
import os
from .json_filter import filter_duplicate_elements


class JsonStorage:

    def save(self, repo, base_name):
        repo = filter_duplicate_elements(repo)
        os.makedirs("output", exist_ok=True)

        path = f"output/{base_name}.json"

        with open(path, "w", encoding="utf-8") as f:
            json.dump(repo, f, indent=4)

        print("Saved ->", path)