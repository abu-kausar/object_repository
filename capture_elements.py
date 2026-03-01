"""
Gmail Signup Page - Object Repository Builder
URL: https://accounts.google.com/signup

This script:
1. Opens Gmail signup page in Chrome
2. Captures all UI elements automatically
3. Stores them in Object Repository (repository.json)
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

GMAIL_SIGNUP_URL = "https://accounts.google.com/signup/v2/createaccount?flowName=GlifWebSignIn&flowEntry=SignUp"

# ── All elements on Gmail Signup Page ─────────────────────
# Format: (element_name, selector, selector_type, element_type)
GMAIL_SIGNUP_ELEMENTS = [
    (
        "First-Name",
        "input[name='firstName']",
        "css",
        "Input"
    ),
    (
        "Last-Name",
        "input[name='lastName']",
        "css",
        "Input"
    ),
    (
        "Username",
        "input[name='Username']",
        "css",
        "Input"
    ),
    # (
    #     "Password",
    #     "input[name='Passwd']",
    #     "css",
    #     "Input"
    # ),
    # (
    #     "Confirm-Password",
    #     "input[name='PasswdAgain']",
    #     "css",
    #     "Input"
    # ),
    (
        "Next-Button",
        "//button[.//span[text()='Next']]",
        "xpath",
        "Button"
    ),
    (
        "Sign-In-Link",
        "//button[.//span[text()='Sign in instead']]",
        "xpath",
        "Link"
    ),
]


def setup_driver():
    """Setup Chrome WebDriver"""
    options = Options()
    # Comment below line if you want to SEE the browser
    # options.add_argument("--headless")
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


def verify_element_exists(driver, wait, selector, selector_type):
    """Check if element actually exists on page"""
    try:
        by = By.CSS_SELECTOR if selector_type == "css" else By.XPATH
        wait.until(EC.presence_of_element_located((by, selector)))
        return True
    except Exception:
        return False


def capture_gmail_signup_elements():
    print("\n" + "="*50)
    print("  Gmail Signup - Object Repository Builder")
    print("="*50)
    print(f"\n Page URL: {GMAIL_SIGNUP_URL}\n")

    # ── Step 1: Setup Repository ───────────────────────────
    print(" Setting up Object Repository...")
    repo = ObjectRepository()
    repo.add_application("GMailApp", version="1.0.0", app_type="Web")
    repo.add_screen(
        "GMailApp",
        "Chrome: GMail Signup",
        url=GMAIL_SIGNUP_URL
    )

    # ── Step 2: Open Browser ───────────────────────────────
    print("\n Opening Gmail Signup Page")
    driver = setup_driver()
    wait = WebDriverWait(driver, 15)

    captured = []
    failed   = []

    try:
        driver.get(GMAIL_SIGNUP_URL)
        print(f"  Page opened: {driver.title}")
        time.sleep(3)  # Let page fully load

        # ── Step 3: Capture Each Element ───────────────────
        print("\n Capturing Elements...\n")

        for elem_name, selector, sel_type, elem_type in GMAIL_SIGNUP_ELEMENTS:
            exists = verify_element_exists(driver, wait, selector, sel_type)
            if exists:
                repo.add_element(
                    "GMailApp",
                    "Chrome: GMail Signup",
                    elem_name,
                    selector,
                    sel_type,
                    elem_type
                )
                captured.append(elem_name)
            else:
                print(f"  Element '{elem_name}' not found on page (may load later)")
                failed.append(elem_name)

        # ── Step 4: Summary ────────────────────────────────
        print(f"\n{'='*50}")
        print(f"  Capture Summary")
        print(f"{'='*50}")
        print(f"  Captured : {len(captured)} elements")
        for c in captured:
            print(f"       → {c}")
        if failed:
            print(f"  ⚠️  Not Found: {len(failed)} elements")
            for f in failed:
                print(f"       → {f}")

    except Exception as e:
        print(f"\n  Error: {e}")

    finally:
        time.sleep(2)
        driver.quit()
        print("\n  Browser closed")

    # ── Step 5: Display Full Repository ───────────────────
    repo.display_repository()
    print("  Repository saved to: repository.json\n")


if __name__ == "__main__":
    capture_gmail_signup_elements()