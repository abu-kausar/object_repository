from playwright.sync_api import sync_playwright


class BrowserManager:

    def start(self):

        self.p = sync_playwright().start()

        self.browser = self.p.chromium.launch(
            headless=False
        )

        self.context = self.browser.new_context()

        self.page = self.context.new_page()

        return self.page, self.context