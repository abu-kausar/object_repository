# UiPath Studio Object Library

This repository contains Python scripts to automatically capture UI elements from web applications (like Gmail and SAP S/4HANA) and generate UiPath-compatible Object Repository files (`.json`). The generated repositories can be imported directly into UiPath Studio to simplify UI automation.

## Project Structure

*   `capture_elements.py`: Script to automate the Google/Gmail login flow and capture UI elements into `gmail_login_repository.json`.
*   `capture_sap.py`: Script to automate a Purchase Requisition process in SAP S/4HANA and capture UI elements into `sap_repository.json`.
*   `inject_elements2.py` / `inject_sap_elements.py`: Utility scripts for injecting captured elements into UiPath projects.
*   `Gmail_UI_Library/`: A sample UiPath Object Library project utilizing the captured Gmail elements.
*   `SAPUILibrary/`: A sample UiPath Object Library project utilizing the captured SAP elements.

## Dependencies

The project requires Python and uses Selenium for browser automation. The dependencies are listed in `requirements.txt`.

*   `selenium`
*   `webdriver-manager`

## How to Run on Any Machine

Follow these simple steps to run the scripts on your machine:

1.  **Install Python:** Ensure you have Python installed on your system (e.g., Python 3.8+).
2.  **Clone or Download this Repository.**
3.  **Open a Terminal/Command Prompt** and navigate to the project directory.
4.  **Install Dependencies:** Run the following command to install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure Credentials & URLs (Important):**
    *   If running `capture_elements.py`: Open the file and update `USER_EMAIL` and `USER_PASS` with your testing credentials. Note: You might need to handle 2FA manually in the browser window if prompted by Google.
    *   If running `capture_sap.py`: Open the file and update the SAP `url`, username, and password logic as needed for your specific SAP S/4HANA instance.

6.  **Run the Scripts:**
    *   To capture Google/Gmail elements and generate the repository:
        ```bash
        python capture_elements.py
        ```
    *   To capture SAP elements and generate the repository:
        ```bash
        python capture_sap.py
        ```

7.  **Import into UiPath:** Once the JSON repository files are generated (`gmail_login_repository.json`, `sap_repository.json`), you can use them directly in your UiPath Object Repository.

## Credits

R&D By Md Rashaduzzaman
Senior Software Engineer
Xyphera Technology.
rashaduzzaman@xypheratech.com
