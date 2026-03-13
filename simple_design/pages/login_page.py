import json
from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        
        with open("object_repository/login_page.json") as f:
            self.locators = json.load(f)

    def get_element(self, name):
        locator = self.locators[name]
        by_type = getattr(By, locator["by"].upper())
        return self.driver.find_element(by_type, locator["value"])

    def enter_username(self, username):
        self.get_element("username_field").send_keys(username)

    def enter_password(self, password):
        self.get_element("password_field").send_keys(password)

    def click_login(self):
        self.get_element("login_button").click()