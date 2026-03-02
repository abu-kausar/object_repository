import json, os, shutil

BASE = r'd:\Leaniar_Devs\object_repository-main\object_repository-main\Gmail_UI_Library'
OBJ  = os.path.join(BASE, '.objects')
DATA = os.path.join(BASE, 'Data')

LIB_ID  = 'ZftEUAJ9MUyMlt_mopmLlw'

S_LOGE  = {'fld':'e2g1', 'id':'e2g1TFksRUWIhQL26EXtMg', 'name':'Login_Email'}
S_LOGP  = {'fld':'OgUK', 'id':'OgUKpTetdkOEBAAHhjTJaw', 'name':'Login_Password'}
S_DASH  = {'fld':'WxKA', 'id':'WxKAw64tfEOEbg1fg8bfXA', 'name':'Gmail_Dashboard'}
S_COMP  = {'fld':'ty3z', 'id':'ty3z0Lt7rkiERCRsLw2NoA', 'name':'Gmail_Compose'}

# Element definitions: Name, ID, Target screen, GUI Type, Selector
ELEMENTS = [
    ('EmailInput',   'EmIn0001000000000001', S_LOGE, 'Input',  "<webctrl id='identifierId' />"),
    ('NextButton',   'NxBt0001000000000001', S_LOGE, 'Button', "<webctrl id='identifierNext' />"),
    ('PasswordInput','PsIn0001000000000001', S_LOGP, 'Input',  "<webctrl tag='INPUT' name='Passwd' />"),
    ('NextButton',   'NxB20001000000000001', S_LOGP, 'Button', "<webctrl id='passwordNext' />"),
    ('Inbox',        'Inbo0001000000000001', S_DASH, 'Link',   "<webctrl tag='A' href='#inbox' />"),
    ('Sent',         'Sen00001000000000001', S_DASH, 'Link',   "<webctrl tag='A' href='#sent' />"),
    ('Drafts',       'Dra00001000000000001', S_DASH, 'Link',   "<webctrl tag='A' href='#drafts' />"),
    ('Spam',         'Spam0001000000000001', S_DASH, 'Link',   "<webctrl tag='A' href='#spam' />"),
    ('Social',       'Soci0001000000000001', S_DASH, 'Link',   "<webctrl tag='A' href='#social' />"),
    ('Compose',      'Com00001000000000001', S_DASH, 'Button', "<webctrl tag='DIV' aaname='Compose' />"),
    ('To',           'ToFi0001000000000001', S_COMP, 'Input',  "<webctrl tag='TEXTAREA' name='to' />"),
    ('Subject',      'SuFi0001000000000001', S_COMP, 'Input',  "<webctrl tag='INPUT' name='subjectbox' />"),
    ('MessageBody',  'BoFi0001000000000001', S_COMP, 'Input',  "<webctrl tag='DIV' aria-label='Message Body' />"),
    ('SendButton',   'SeBu0001000000000001', S_COMP, 'Button', "<webctrl tag='DIV' aaname='Send' role='button' />"),
]

CB = ['UiPath.Platform, Version=24.10.0.0, Culture=neutral, PublicKeyToken=null']
print('Injecting 12 elements into the validated screens...')

# Read existing UiDescriptors.json
src = os.path.join(OBJ, 'UiDescriptors.json')
with open(src, 'r', encoding='utf-8') as f:
    desc = json.load(f)

# Find screens in the JSON
screens = desc['Applications'][0]['Screens']
scmap = {s['Id']: s for s in screens}

for name, eid, scr, etype, sel in ELEMENTS:
    efld = eid[:4] # First 4 chars become folder name
    p = f'{OBJ}/5_eF/tjZw/{scr["fld"]}/{efld}'
    os.makedirs(p, exist_ok=True)
    
    # 1. Write element .metadata
    md = {'Name':name, 'Type':'Descriptor', 'Id':eid, 'Reference':f'{LIB_ID}/{eid}', 'ParentRef':f'{LIB_ID}/{scr["id"]}', 'CreatedBy':CB}
    with open(f'{p}/.metadata', 'w', encoding='utf-8') as f: json.dump(md, f, indent=2)
    
    # 2. Write element .type
    with open(f'{p}/.type', 'w', encoding='utf-8') as f: f.write('Descriptor')
    
    # 3. Add to matching Screen in JSON
    # Be careful not to add it twice if the script is run twice
    existing = [x for x in scmap[scr['id']]['UIElements'] if x['Id'] == eid]
    if not existing:
        scmap[scr['id']]['UIElements'].append({
            'Id': eid,
            'Name': name,
            'DisplayName': name.replace('Button', '').replace('Input', ' Input').strip() if name != 'Compose' else 'Compose',
            'Type': etype,
            'Selector': {'Type': 'Selector', 'Value': sel}
        })
    print(f'  Added {name} -> {scr["name"]}')

# Save updated JSON files
with open(src, 'w', encoding='utf-8') as f: json.dump(desc, f, indent=2)
os.makedirs(DATA, exist_ok=True)
shutil.copy(src, os.path.join(DATA, 'UiDescriptors.json'))
shutil.copy(src, os.path.join(BASE, 'Objects.json'))

# Clear generic caches
for c in ['.local', '.settings', '.tmh']:
    p = os.path.join(BASE, c)
    if os.path.exists(p): shutil.rmtree(p)

print('\nSuccessfully injected elements and safely updated UiDescriptors.json.')
