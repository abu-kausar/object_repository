import json
import os
import uuid
from datetime import datetime

REPO_FILE = "repository.json"

class ObjectRepository:
    """
    Python implementation of UiPath-style Object Repository.
    Stores UI elements in structured format: 
    Applications > Screens > UIElements
    """

    def __init__(self, filename="repository.json"):
        self.filename = filename
        self.repo = self.load()
        if "Applications" not in self.repo:
            self.repo = {"SchemaVersion": "4.0", "Applications": []}

    def load(self):
        """Load existing repository from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"SchemaVersion": "4.0", "Applications": []}

    def save(self):
        """Save repository to JSON file"""
        with open(self.filename, "w") as f:
            json.dump(self.repo, f, indent=4)

    def add_application(self, app_name, version="1.0.0", app_type="Web"):
        """Add a new application if it doesn't exist"""
        for app in self.repo["Applications"]:
            if app["Name"] == app_name:
                print(f"   Application '{app_name}' already exists!")
                return
        
        new_app = {
            "Id": str(uuid.uuid4()),
            "Name": app_name,
            "Version": version,
            "Type": app_type,
            "CreatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Screens": []
        }
        self.repo["Applications"].append(new_app)
        self.save()
        print(f"   Application '{app_name}' added (v{version})")

    def add_screen(self, app_name, screen_name, url=""):
        """Add a screen under application"""
        app = next((a for a in self.repo["Applications"] if a["Name"] == app_name), None)
        if not app:
            print(f"  Application '{app_name}' not found!")
            return

        for screen in app["Screens"]:
            if screen["Name"] == screen_name:
                print(f"  Screen '{screen_name}' already exists!")
                return

        new_screen = {
            "Id": str(uuid.uuid4()),
            "Name": screen_name,
            "DisplayName": screen_name,
            "URL": url,
            "UIElements": []
        }
        app["Screens"].append(new_screen)
        self.save()
        print(f"  Screen '{screen_name}' added")

    def add_element(self, app_name, screen_name, element_name,
                    selector, selector_type="CssSelector", element_type="Input"):
        """Add a UI element under screen"""
        app = next((a for a in self.repo["Applications"] if a["Name"] == app_name), None)
        if not app: return
        
        screen = next((s for s in app["Screens"] if s["Name"] == screen_name), None)
        if not screen: return

        # Update if exists, else append
        for elem in screen["UIElements"]:
            if elem["Name"] == element_name:
                elem["Selector"] = {"Type": selector_type, "Value": selector}
                elem["LastUpdated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save()
                print(f"  Element '{element_name}' updated")
                return

        new_elem = {
            "Id": str(uuid.uuid4()),
            "Name": element_name,
            "DisplayName": element_name,
            "Type": element_type,
            "Selector": {
                "Type": selector_type,
                "Value": selector
            },
            "CapturedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        screen["UIElements"].append(new_elem)
        self.save()
        print(f"  Element '{element_name}' captured & stored")

    def display_repository(self):
        """Display full Object Repository structure"""
        print("\n" + "="*50)
        print("       OBJECT REPOSITORY (UiPath Format)")
        print("="*50)
        for app in self.repo.get("Applications", []):
            print(f"\n   Application : {app['Name']} (v{app['Version']})")
            for screen in app.get("Screens", []):
                print(f"     Screen : {screen['Name']}")
                for elem in screen.get("UIElements", []):
                    print(f"        - {elem['Name']} [{elem['Type']}]")
                    print(f"          Selector: {elem['Selector']['Value']} ({elem['Selector']['Type']})")
        print("\n" + "="*50 + "\n")