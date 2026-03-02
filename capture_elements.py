"""
Google Login & Gmail - Object Repository Builder
URL: https://accounts.google.com

This script:
1. Opens Google login page
2. Guides user through login (handling multiple screens)
3. Captures Gmail elements (Inbox, Drafts, Sent)
4. Stores them in UiPath-compatible Object Repository
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from object_repository import ObjectRepository
import time

GOOGLE_LOGIN_URL = "https://accounts.google.com/ServiceLogin?service=mail"

# Definitions for Login and Gmail elements
LOGIN_ELEMENTS = {
    "Email": ("identifierId", "id", "Input"),
    "EmailNext": ("identifierNext", "id", "Button"),
    "Password": ("input[name='Passwd']", "css", "Input"),
    "PasswordNext": ("passwordNext", "id", "Button")
}
GMAIL_DASHBOARD_ELEMENTS = {
    "Inbox": ("//a[contains(@href, '#inbox')]", "xpath", "Link"),
    "Sent": ("//a[contains(@href, '#sent')]", "xpath", "Link"),
    "Drafts": ("//a[contains(@href, '#drafts')]", "xpath", "Link"),
    "Compose": ("//div[text()='Compose']", "xpath", "Button")
}

COMPOSE_WINDOW_ELEMENTS = {
    "To": ("textarea[name='to']", "css", "Input"),
    "Subject": ("input[name='subjectbox']", "css", "Input"),
    "MessageBody": ("div[aria-label='Message Body']", "css", "Input"),
    "SendButton": ("//div[text()='Send' and @role='button']", "xpath", "Button")
}

def setup_driver():
    """Setup Chrome WebDriver"""
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

def wait_and_capture(driver, wait, repo, app_name, screen_name, element_name, selector, sel_type, elem_type):
    """Wait for element and capture it if found"""
    try:
        by = By.ID if sel_type == "id" else (By.CSS_SELECTOR if sel_type == "css" else By.XPATH)
        wait.until(EC.presence_of_element_located((by, selector)))
        
        # UIPath style selector names
        uipath_sel_type = "CssSelector" if sel_type == "css" else ("Id" if sel_type == "id" else "XmlPath")
        
        repo.add_element(app_name, screen_name, element_name, selector, uipath_sel_type, elem_type)
        return True
    except Exception:
        print(f"  Warning: Could not capture '{element_name}'")
        return False

def capture_google_login_flow():
    print("\n" + "="*50)
    print("  Google Login & Gmail - Object Repository Builder")
    print("="*50)

    # Use a separate repository file for Gmail login
    repo = ObjectRepository(filename="gmail_login_repository.json")
    app_id = "GoogleWorkspace"
    repo.add_application(app_id, version="1.0.0", app_type="Web")

    driver = setup_driver()
    wait = WebDriverWait(driver, 30)

    # Credentials
    USER_EMAIL = "illuminati011111@gmail.com"
    USER_PASS  = "Mdrrana32!"

    try:
        # --- PHASE 1: LOGIN (EMAIL) ---
        print("\n [Step 1] Initializing Login Screen...")
        driver.get(GOOGLE_LOGIN_URL)
        repo.add_screen(app_id, "Login: Email", url=driver.current_url)
        
        # Capture & Enter Email
        sel, stype, etype = LOGIN_ELEMENTS["Email"]
        wait_and_capture(driver, wait, repo, app_id, "Login: Email", "EmailInput", sel, stype, etype)
        driver.find_element(By.ID, sel).send_keys(USER_EMAIL)
        
        sel, stype, etype = LOGIN_ELEMENTS["EmailNext"]
        wait_and_capture(driver, wait, repo, app_id, "Login: Email", "NextButton", sel, stype, etype)
        driver.find_element(By.ID, sel).click()

        # Wait for Password field
        time.sleep(3)
        print("\n [Step 2] Initializing Password Screen...")
        repo.add_screen(app_id, "Login: Password", url=driver.current_url)

        # Capture & Enter Password
        sel, stype, etype = LOGIN_ELEMENTS["Password"]
        wait_and_capture(driver, wait, repo, app_id, "Login: Password", "PasswordInput", sel, stype, etype)
        driver.find_element(By.CSS_SELECTOR, sel).send_keys(USER_PASS)

        sel, stype, etype = LOGIN_ELEMENTS["PasswordNext"]
        wait_and_capture(driver, wait, repo, app_id, "Login: Password", "NextButton", sel, stype, etype)
        driver.find_element(By.ID, sel).click()

        print("\n  PLEASE LOG IN IN THE BROWSER WINDOW IF PROMPTED BY PHONE.")
        print("  Waiting for login success (Gmail Dashboard)...")

        # --- PHASE 2: GMAIL DASHBOARD ---
        # Wait for inbox to appear (indicator of login success)
        inbox_sel = GMAIL_DASHBOARD_ELEMENTS["Inbox"][0]
        # Using a fresh wait with longer timeout for 2FA
        dashboard_wait = WebDriverWait(driver, 120)
        dashboard_wait.until(EC.presence_of_element_located((By.XPATH, inbox_sel)))
        print("\n [Step 2] Login Successful. Accessing Gmail Dashboard.")
        
        repo.add_screen(app_id, "Gmail: Dashboard", url=driver.current_url)

        print("\n Capturing Gmail Elements...\n")
        for name, (sel, stype, etype) in GMAIL_DASHBOARD_ELEMENTS.items():
            if wait_and_capture(driver, wait, repo, app_id, "Gmail: Dashboard", name, sel, stype, etype):
                print(f"  Successfully captured: {name}")

        # --- PHASE 3: COMPOSE WINDOW ---
        print("\n [Step 3] Opening Compose Window...")
        compose_btn_sel = GMAIL_DASHBOARD_ELEMENTS["Compose"][0]
        driver.find_element(By.XPATH, compose_btn_sel).click()
        
        print("\n Initializing Compose Screen...")
        repo.add_screen(app_id, "Gmail: Compose", url=driver.current_url)

        print("\n Capturing Compose Elements...\n")
        # Wait a bit for window to pop up
        time.sleep(2)
        for name, (sel, stype, etype) in COMPOSE_WINDOW_ELEMENTS.items():
            if wait_and_capture(driver, wait, repo, app_id, "Gmail: Compose", name, sel, stype, etype):
                print(f"  Successfully captured: {name}")

    except Exception as e:
        print(f"\n Error occurred: {e}")

    finally:
        print("\n Summary of Repository:")
        repo.display_repository()
        print(f" Repository saved to: {repo.filename}")
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    capture_google_login_flow()