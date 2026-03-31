import os


class ScreenshotService:

    def take(self, page, base_name, screen_name):

        dir_path = f"output/screenshots/{base_name}"

        os.makedirs(dir_path, exist_ok=True)

        path = f"{dir_path}/{screen_name}.png"

        page.screenshot(
            path=path,
            full_page=True
        )

        print("Screenshot ->", path)