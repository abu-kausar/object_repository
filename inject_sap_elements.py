import json, os, shutil, uuid

BASE = r'd:\Leaniar_Devs\object_repository-main\object_repository-main\SAPUILibrary'
OBJ  = os.path.join(BASE, '.objects')
DATA = os.path.join(BASE, 'Data')

# Studio-generated IDs mapped from the folder structure:
LIB_ID = 'CzpS0zKua0iQdKHLw-uqIg'
APP_ID = '0BFW7D_wE06pk3NHpQqBAQ'
VER_ID = 'M4w7dx0nhkCaSarcCbg-BQ'

# Map Screen Names to their Studio IDs & Folder Names
STUDIO_SCREENS = {
    'SAP_Login':     { 'id': '_6Wmg6PUuke9xxihmeXD2A', 'fld': '_6Wm' },
    'SAP_Home':      { 'id': 'O1gL-cPw-UiE9sWd71q2Hg', 'fld': 'O1gL' },
    'SAP_Manage_PR': { 'id': '62mHfywoVkuo3ivf_c6PuQ', 'fld': '62mH' },
    'SAP_PR_Item':   { 'id': 'dY9XV8btY02ASsGnTAu91Q', 'fld': 'dY9X' },
    'SAP_PR_Submit': { 'id': '0QDtAtkmpEuOkV8qT6ESoQ', 'fld': '0QDt' }
}

CB = ['UiPath.Platform, Version=25.12.1.0, Culture=neutral, PublicKeyToken=null']

print('Injecting SAP Elements...')

# 1. Load captured elements from sap_repository.json
with open(r'd:\Leaniar_Devs\object_repository-main\object_repository-main\sap_repository.json', 'r', encoding='utf-8') as f:
    repo = json.load(f)

# The repo has Screens and inside each Screen we have UIElements.
source_screens = repo['Applications'][0]['Screens']

# Prepare the UiDescriptors.json structure
desc = {'SchemaVersion': '4.0', 'Applications': [
    {'Id': APP_ID, 'Name': 'SAP_S4HANA', 'Version': '1.0.0', 'Type': 'Web', 'Screens': []}
]}

# Initialize empty screen structures in the JSON
scmap = {}
for s_name, s_data in STUDIO_SCREENS.items():
    # Find the corresponding source screen for url/displayname
    src_sc = next((s for s in source_screens if s['Name'] == s_name), None)
    if not src_sc: continue
    
    scmap[s_name] = {
        'Id': s_data['id'],
        'Name': s_name,
        'DisplayName': src_sc['DisplayName'],
        'URL': src_sc['URL'],
        'UIElements': []
    }

for src_sc in source_screens:
    s_name = src_sc['Name']
    if s_name not in STUDIO_SCREENS: continue
    
    studio_fld = STUDIO_SCREENS[s_name]['fld']
    studio_id  = STUDIO_SCREENS[s_name]['id']
    
    print(f"\nProcessing Screen: {s_name} (Studio ID: {studio_id})")
    
    for el in src_sc['UIElements']:
        el_name = el['Name']
        el_type = el['Type']
        el_sel  = el['Selector']
        
        # We need a 22-char Base64url-like ID that matches UiPath structure.
        # But wait, we MUST follow the rule that first 4 chars == folder name!
        # So we generate an ID like 'EmIn0001000000000001' where 'EmIn' is folder.
        
        # Take first 4 chars of name for folder (pad if needed)
        fld_chars = (el_name[:4] + "0000")[:4].replace('_', 'x')
        eid = f"{fld_chars}0001000000000001"
        
        # If ID collision (e.g. multiple buttons starting with same chars), find a unique one
        while any(x for x in scmap[s_name]['UIElements'] if x['Id'] == eid):
            fld_chars = fld_chars[:3] + str(int(fld_chars[3]) + 1 if fld_chars[3].isdigit() else 1)
            eid = f"{fld_chars}0001000000000001"
            
        p = f'{OBJ}/0BFW/M4w7/{studio_fld}/{fld_chars}'
        os.makedirs(p, exist_ok=True)
        
        # Write .metadata
        md = {
            'Name': el_name,
            'Type': 'Descriptor',
            'Id': eid,
            'Reference': f'{LIB_ID}/{eid}',
            'ParentRef': f'{LIB_ID}/{studio_id}',
            'CreatedBy': CB
        }
        with open(f'{p}/.metadata', 'w', encoding='utf-8') as f: json.dump(md, f, indent=2)
        
        # Write .type
        with open(f'{p}/.type', 'w', encoding='utf-8') as f: f.write('Descriptor')
        
        # Add to UiDescriptors JSON
        scmap[s_name]['UIElements'].append({
            'Id': eid,
            'Name': el_name,
            'DisplayName': el['DisplayName'],
            'Type': el_type,
            'Selector': el_sel
        })
        print(f'  Added {el_name} -> {fld_chars}')

# Add screens back to description payload
for k,v in scmap.items():
    desc['Applications'][0]['Screens'].append(v)

# Write output files
src = os.path.join(OBJ, 'UiDescriptors.json')
with open(src, 'w', encoding='utf-8') as f: json.dump(desc, f, indent=2)

os.makedirs(DATA, exist_ok=True)
shutil.copy(src, os.path.join(DATA, 'UiDescriptors.json'))
shutil.copy(src, os.path.join(BASE, 'Objects.json'))

# Clear local cache to force reload
for c in ['.local', '.settings', '.tmh']:
    p = os.path.join(BASE, c)
    if os.path.exists(p): shutil.rmtree(p)

print('\nDone! Successfully injected SAP elements and built UiDescriptors.json.')
