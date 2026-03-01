import json
import os
import uuid
from datetime import datetime

REPO_FILE = "repository.json"

class ObjectRepository:
    """
    Python implementation of UiPath-style Object Repository.
    Stores UI elements in structured format: 
    Application > Version > Screen > Elements
    """

    def __init__(self):
        self.repo = self.load()

    def load(self):
        """Load existing repository from JSON file"""
        if os.path.exists(REPO_FILE):
            with open(REPO_FILE, "r") as f:
                return json.load(f)
        return {}

    def save(self):
        """Save repository to JSON file"""
        with open(REPO_FILE, "w") as f:
            json.dump(self.repo, f, indent=4)

    def add_application(self, app_name, version="1.0.0", app_type="Web"):
        """Add a new application (like UiPath Add Application)"""
        if app_name not in self.repo:
            self.repo[app_name] = {
                "version": version,
                "type": app_type,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "screens": {}
            }
            self.save()
            print(f"   Application '{app_name}' added (v{version})")
        else:
            print(f"   Application '{app_name}' already exists!")

    def add_screen(self, app_name, screen_name, url=""):
        """Add a screen under application (like UiPath Add Screen)"""
        if app_name not in self.repo:
            print(f"  Application '{app_name}' not found!")
            return
        if screen_name not in self.repo[app_name]["screens"]:
            self.repo[app_name]["screens"][screen_name] = {
                "url": url,
                "elements": {}
            }
            self.save()
            print(f"  Screen '{screen_name}' added")
        else:
            print(f"  Screen '{screen_name}' already exists!")

    def add_element(self, app_name, screen_name, element_name,
                    selector, selector_type="css", element_type="Input"):
        """Add a UI element (like UiPath Capture Element)"""
        try:
            self.repo[app_name]["screens"][screen_name]["elements"][element_name] = {
                "id": str(uuid.uuid4()),          # unique ID like UiPath GUID
                "selector": selector,
                "selector_type": selector_type,   # css or xpath
                "element_type": element_type,     # Input, Button, Text etc
                "captured_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.save()
            print(f"  Element '{element_name}' captured & stored")
        except KeyError as e:
            print(f"  Error: {e} not found!")

    def get_element(self, app_name, screen_name, element_name):
        """Retrieve a UI element from repository"""
        try:
            return self.repo[app_name]["screens"][screen_name]["elements"][element_name]
        except KeyError:
            print(f"  Element '{element_name}' not found!")
            return None

    def display_repository(self):
        """Display full Object Repository structure like UiPath panel"""
        print("\n" + "="*50)
        print("       OBJECT REPOSITORY")
        print("="*50)
        for app, app_data in self.repo.items():
            print(f"\n   Application : {app}")
            print(f"     Version     : {app_data['version']}")
            print(f"     Type        : {app_data['type']}")
            print(f"     Created     : {app_data['created_at']}")
            for screen, screen_data in app_data["screens"].items():
                print(f"\n     🖥️  Screen : {screen}")
                print(f"          URL  : {screen_data['url']}")
                print(f"          Elements:")
                for elem, elem_data in screen_data["elements"].items():
                    print(f"\n          🔹 {elem}")
                    print(f"               ID            : {elem_data['id']}")
                    print(f"               Type          : {elem_data['element_type']}")
                    print(f"               Selector Type : {elem_data['selector_type']}")
                    print(f"               Selector      : {elem_data['selector']}")
                    print(f"               Captured At   : {elem_data['captured_at']}")
        print("\n" + "="*50 + "\n")