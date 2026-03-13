from selenium import webdriver
from pages.login_page import LoginPage

driver = webdriver.Chrome()
driver.get("https://example.com/login")

login = LoginPage(driver)
login.enter_username("admin")
login.enter_password("1234")
login.click_login()