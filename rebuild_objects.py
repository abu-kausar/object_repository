"""
Rebuilds the Gmail_UI_Library/.objects directory from scratch
using cryptographically correct UiPath-compatible base64 IDs
and the exact file structure UiPath Studio expects.
"""
import os
import json
import shutil
import base64
import hashlib

BASE_DIR = r"d:\Leaniar_Devs\object_repository-main\object_repository-main\Gmail_UI_Library"
OBJECTS_DIR = os.path.join(BASE_DIR, ".objects")

def make_id(seed: str) -> str:
    """Generate a stable 22-char base64 ID from a seed string (like UiPath does)."""
    digest = hashlib.md5(seed.encode()).digest()
    b64 = base64.urlsafe_b64encode(digest).decode().rstrip("=")
    return b64  # 22 chars

def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  Wrote: {os.path.relpath(path, BASE_DIR)}")

def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def rebuild():
    # ---- Generate IDs -----
    LIB_ID  = make_id("Gmail_UI_Library")           # library root id
    APP_ID  = make_id("Google_Workspace_App")
    VER_ID  = make_id("Google_Workspace_v1.0.0")

    SCR_LOGIN_EMAIL_ID  = make_id("Screen_Login_Email")
    SCR_LOGIN_PASS_ID   = make_id("Screen_Login_Password")
    SCR_DASHBOARD_ID    = make_id("Screen_Gmail_Dashboard")
    SCR_COMPOSE_ID      = make_id("Screen_Gmail_Compose")

    EL_EMAIL_INPUT_ID   = make_id("El_EmailInput")
    EL_EMAIL_NEXT_ID    = make_id("El_EmailNext")
    EL_PASS_INPUT_ID    = make_id("El_PasswordInput")
    EL_PASS_NEXT_ID     = make_id("El_PasswordNext")
    EL_INBOX_ID         = make_id("El_Inbox")
    EL_SENT_ID          = make_id("El_Sent")
    EL_DRAFTS_ID        = make_id("El_Drafts")
    EL_COMPOSE_ID       = make_id("El_Compose_btn")
    EL_TO_ID            = make_id("El_ComposeTo")
    EL_SUBJECT_ID       = make_id("El_ComposeSubject")
    EL_BODY_ID          = make_id("El_ComposeBody")
    EL_SEND_ID          = make_id("El_ComposeSend")

    # Short folder names (first 4 chars of ID)
    app_folder  = APP_ID[:4]
    ver_folder  = VER_ID[:4]

    scr_email_folder  = SCR_LOGIN_EMAIL_ID[:4]
    scr_pass_folder   = SCR_LOGIN_PASS_ID[:4]
    scr_dash_folder   = SCR_DASHBOARD_ID[:4]
    scr_comp_folder   = SCR_COMPOSE_ID[:4]

    el_folders = {
        EL_EMAIL_INPUT_ID: (scr_email_folder, "EmailInput"),
        EL_EMAIL_NEXT_ID:  (scr_email_folder, "NextButton_Email"),
        EL_PASS_INPUT_ID:  (scr_pass_folder,  "PasswordInput"),
        EL_PASS_NEXT_ID:   (scr_pass_folder,  "NextButton_Pass"),
        EL_INBOX_ID:       (scr_dash_folder,  "Inbox"),
        EL_SENT_ID:        (scr_dash_folder,  "Sent"),
        EL_DRAFTS_ID:      (scr_dash_folder,  "Drafts"),
        EL_COMPOSE_ID:     (scr_dash_folder,  "Compose"),
        EL_TO_ID:          (scr_comp_folder,  "To"),
        EL_SUBJECT_ID:     (scr_comp_folder,  "Subject"),
        EL_BODY_ID:        (scr_comp_folder,  "MessageBody"),
        EL_SEND_ID:        (scr_comp_folder,  "SendButton"),
    }

    print(f"\n  Library ID   : {LIB_ID}")
    print(f"  App ID       : {APP_ID}")
    print(f"  Ver ID       : {VER_ID}")

    # ---- Wipe and rebuild .objects ----
    if os.path.exists(OBJECTS_DIR):
        shutil.rmtree(OBJECTS_DIR)
        print(f"\n  Removed old .objects directory")
    os.makedirs(OBJECTS_DIR)

    # ROOT .metadata
    write_json(os.path.join(OBJECTS_DIR, ".metadata"), {
        "Type": "Library",
        "Id": LIB_ID,
        "CreatedBy": ["UiPath.Platform, Version=24.10.0.0, Culture=neutral, PublicKeyToken=null"]
    })

    # APPLICATION folder
    app_path = os.path.join(OBJECTS_DIR, app_folder)
    os.makedirs(app_path, exist_ok=True)
    write_json(os.path.join(app_path, ".metadata"), {
        "Name": "Google_Workspace",
        "Type": "Application",
        "Id": APP_ID,
        "Reference": f"{LIB_ID}/{APP_ID}",
        "ParentRef": LIB_ID,
        "CreatedBy": ["UiPath.Platform, Version=24.10.0.0, Culture=neutral, PublicKeyToken=null"]
    })

    # VERSION folder
    ver_path = os.path.join(app_path, ver_folder)
    os.makedirs(ver_path, exist_ok=True)
    write_json(os.path.join(ver_path, ".metadata"), {
        "Name": "v1.0.0",
        "Type": "ApplicationVersion",
        "Id": VER_ID,
        "Reference": f"{LIB_ID}/{VER_ID}",
        "ParentRef": f"{LIB_ID}/{APP_ID}",
        "CreatedBy": ["UiPath.Platform, Version=24.10.0.0, Culture=neutral, PublicKeyToken=null"]
    })

    # SCREENS
    screens = [
        (SCR_LOGIN_EMAIL_ID,  scr_email_folder, "Login_Email",     "https://accounts.google.com/", "Screen"),
        (SCR_LOGIN_PASS_ID,   scr_pass_folder,  "Login_Password",  "https://accounts.google.com/", "Screen"),
        (SCR_DASHBOARD_ID,    scr_dash_folder,  "Gmail_Dashboard", "https://mail.google.com/",     "Screen"),
        (SCR_COMPOSE_ID,      scr_comp_folder,  "Gmail_Compose",   "https://mail.google.com/",     "Screen"),
    ]
    for scr_id, scr_folder, scr_name, scr_url, scr_type in screens:
        scr_path = os.path.join(ver_path, scr_folder)
        os.makedirs(scr_path, exist_ok=True)
        write_json(os.path.join(scr_path, ".metadata"), {
            "Name": scr_name,
            "Description": scr_url,
            "Type": scr_type,
            "Id": scr_id,
            "Reference": f"{LIB_ID}/{scr_id}",
            "ParentRef": f"{LIB_ID}/{VER_ID}",
            "CreatedBy": ["UiPath.Platform, Version=24.10.0.0, Culture=neutral, PublicKeyToken=null"]
        })
        write_text(os.path.join(scr_path, ".type"), "Screen")

    # ELEMENTS
    elements_meta = {
        EL_EMAIL_INPUT_ID: ("EmailInput",      SCR_LOGIN_EMAIL_ID),
        EL_EMAIL_NEXT_ID:  ("NextButton",      SCR_LOGIN_EMAIL_ID),
        EL_PASS_INPUT_ID:  ("PasswordInput",   SCR_LOGIN_PASS_ID),
        EL_PASS_NEXT_ID:   ("NextButton",      SCR_LOGIN_PASS_ID),
        EL_INBOX_ID:       ("Inbox",           SCR_DASHBOARD_ID),
        EL_SENT_ID:        ("Sent",            SCR_DASHBOARD_ID),
        EL_DRAFTS_ID:      ("Drafts",          SCR_DASHBOARD_ID),
        EL_COMPOSE_ID:     ("Compose",         SCR_DASHBOARD_ID),
        EL_TO_ID:          ("To",              SCR_COMPOSE_ID),
        EL_SUBJECT_ID:     ("Subject",         SCR_COMPOSE_ID),
        EL_BODY_ID:        ("MessageBody",     SCR_COMPOSE_ID),
        EL_SEND_ID:        ("SendButton",      SCR_COMPOSE_ID),
    }

    # Map screen ID to folder
    scr_id_to_folder = {
        SCR_LOGIN_EMAIL_ID: scr_email_folder,
        SCR_LOGIN_PASS_ID:  scr_pass_folder,
        SCR_DASHBOARD_ID:   scr_dash_folder,
        SCR_COMPOSE_ID:     scr_comp_folder,
    }

    for el_id, (el_name, parent_scr_id) in elements_meta.items():
        scr_folder = scr_id_to_folder[parent_scr_id]
        el_folder_name = el_id[:4]
        el_path = os.path.join(ver_path, scr_folder, el_folder_name)
        os.makedirs(el_path, exist_ok=True)
        write_json(os.path.join(el_path, ".metadata"), {
            "Name": el_name,
            "Type": "Descriptor",
            "Id": el_id,
            "Reference": f"{LIB_ID}/{el_id}",
            "ParentRef": f"{LIB_ID}/{parent_scr_id}",
            "CreatedBy": ["UiPath.Platform, Version=24.10.0.0, Culture=neutral, PublicKeyToken=null"]
        })
        write_text(os.path.join(el_path, ".type"), "Descriptor")

    # Build UiDescriptors.json
    descriptor = {
        "SchemaVersion": "4.0",
        "Applications": [{
            "Id": APP_ID,
            "Name": "Google_Workspace",
            "Version": "1.0.0",
            "Type": "Web",
            "Screens": [
                {
                    "Id": SCR_LOGIN_EMAIL_ID,
                    "Name": "Login_Email",
                    "DisplayName": "Login Email",
                    "URL": "https://accounts.google.com/",
                    "UIElements": [
                        {"Id": EL_EMAIL_INPUT_ID, "Name": "EmailInput",  "DisplayName": "Email Input",  "Type": "Input",
                         "Selector": {"Type": "Selector", "Value": "<webctrl id='identifierId' />"}},
                        {"Id": EL_EMAIL_NEXT_ID,  "Name": "NextButton",  "DisplayName": "Next Button",  "Type": "Button",
                         "Selector": {"Type": "Selector", "Value": "<webctrl id='identifierNext' />"}}
                    ]
                },
                {
                    "Id": SCR_LOGIN_PASS_ID,
                    "Name": "Login_Password",
                    "DisplayName": "Login Password",
                    "URL": "https://accounts.google.com/",
                    "UIElements": [
                        {"Id": EL_PASS_INPUT_ID, "Name": "PasswordInput", "DisplayName": "Password Input", "Type": "Input",
                         "Selector": {"Type": "Selector", "Value": "<webctrl tag='INPUT' name='Passwd' />"}},
                        {"Id": EL_PASS_NEXT_ID,  "Name": "NextButton",    "DisplayName": "Next Button",    "Type": "Button",
                         "Selector": {"Type": "Selector", "Value": "<webctrl id='passwordNext' />"}}
                    ]
                },
                {
                    "Id": SCR_DASHBOARD_ID,
                    "Name": "Gmail_Dashboard",
                    "DisplayName": "Gmail Dashboard",
                    "URL": "https://mail.google.com/",
                    "UIElements": [
                        {"Id": EL_INBOX_ID,   "Name": "Inbox",   "DisplayName": "Inbox Link",     "Type": "Link",
                         "Selector": {"Type": "Selector", "Value": "<webctrl tag='A' href='#inbox' />"}},
                        {"Id": EL_SENT_ID,    "Name": "Sent",    "DisplayName": "Sent Link",      "Type": "Link",
                         "Selector": {"Type": "Selector", "Value": "<webctrl tag='A' href='#sent' />"}},
                        {"Id": EL_DRAFTS_ID,  "Name": "Drafts",  "DisplayName": "Drafts Link",    "Type": "Link",
                         "Selector": {"Type": "Selector", "Value": "<webctrl tag='A' href='#drafts' />"}},
                        {"Id": EL_COMPOSE_ID, "Name": "Compose", "DisplayName": "Compose Button",  "Type": "Button",
                         "Selector": {"Type": "Selector", "Value": "<webctrl tag='DIV' aaname='Compose' />"}}
                    ]
                },
                {
                    "Id": SCR_COMPOSE_ID,
                    "Name": "Gmail_Compose",
                    "DisplayName": "Gmail Compose",
                    "URL": "https://mail.google.com/",
                    "UIElements": [
                        {"Id": EL_TO_ID,      "Name": "To",          "DisplayName": "Recipient To",  "Type": "Input",
                         "Selector": {"Type": "Selector", "Value": "<webctrl tag='TEXTAREA' name='to' />"}},
                        {"Id": EL_SUBJECT_ID, "Name": "Subject",     "DisplayName": "Subject Input", "Type": "Input",
                         "Selector": {"Type": "Selector", "Value": "<webctrl tag='INPUT' name='subjectbox' />"}},
                        {"Id": EL_BODY_ID,    "Name": "MessageBody", "DisplayName": "Message Body",  "Type": "Input",
                         "Selector": {"Type": "Selector", "Value": "<webctrl tag='DIV' aria-label='Message Body' />"}},
                        {"Id": EL_SEND_ID,    "Name": "SendButton",  "DisplayName": "Send Button",   "Type": "Button",
                         "Selector": {"Type": "Selector", "Value": "<webctrl tag='DIV' aaname='Send' role='button' />"}}
                    ]
                }
            ]
        }]
    }

    desc_path = os.path.join(OBJECTS_DIR, "UiDescriptors.json")
    with open(desc_path, "w", encoding="utf-8") as f:
        json.dump(descriptor, f, indent=2)
    shutil.copy(desc_path, os.path.join(BASE_DIR, "Objects.json"))
    shutil.copy(desc_path, os.path.join(BASE_DIR, "Data", "UiDescriptors.json"))
    print(f"\n  UiDescriptors.json written & synced to Objects.json and Data/")

    # Clean caches
    for cache in [".local", ".settings", ".tmh", ".project"]:
        p = os.path.join(BASE_DIR, cache)
        if os.path.exists(p):
            shutil.rmtree(p)
            print(f"  Cleared cache: {cache}")

    print("\n  === REBUILD COMPLETE ===")
    print(f"  Library ID: {LIB_ID}")
    print(f"  App ID    : {APP_ID}")
    print(f"\n  Now CLOSE UiPath Studio and REOPEN the project.")

if __name__ == "__main__":
    rebuild()
