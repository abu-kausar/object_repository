# """
# Universal Web Object Repository Generator
# - Uses Playwright (like UiPath, not Selenium)
# - Dynamically scans ALL elements (no hardcoding)
# - Scores elements by importance
# Usage: python object_repo.py https://any-url.com
# """

# import json, os, sys, uuid, asyncio
# from datetime import datetime
# from urllib.parse import urlparse
# from playwright.async_api import async_playwright

# OUTPUT_DIR = "repositories"

# # Dynamic scan — NO hardcoded tags
# # We scan everything and score it
# DYNAMIC_SCAN_SCRIPT = """
# () => {
#     const results = [];
    
#     // Get ALL elements on page dynamically
#     const allElements = document.querySelectorAll('*');
    
#     allElements.forEach((el, index) => {
#         // Skip invisible elements
#         const style = window.getComputedStyle(el);
#         if (style.display === 'none' || 
#             style.visibility === 'hidden' || 
#             style.opacity === '0') return;
        
#         const rect = el.getBoundingClientRect();
#         if (rect.width < 5 || rect.height < 5) return;
        
#         const tag = el.tagName.toLowerCase();
        
#         // ── Score element by interactivity ──────────
#         let score = 0;
        
#         // Interactive tags get high score
#         const interactiveTags = ['input','button','a','select','textarea','form'];
#         if (interactiveTags.includes(tag)) score += 10;
        
#         // Has event listeners
#         if (el.onclick || el.onchange || el.onsubmit) score += 5;
        
#         // Has role attribute
#         const role = el.getAttribute('role');
#         if (role && ['button','link','textbox','checkbox',
#                      'combobox','menuitem'].includes(role)) score += 8;
        
#         // Has aria attributes
#         if (el.getAttribute('aria-label') || 
#             el.getAttribute('aria-labelledby')) score += 3;
        
#         // Has name (form field)
#         if (el.getAttribute('name')) score += 5;
        
#         // Has placeholder (input field)
#         if (el.getAttribute('placeholder')) score += 4;
        
#         // Has data-testid (dev marked it important)
#         if (el.getAttribute('data-testid')) score += 6;
        
#         // Has tabindex (keyboard navigable)
#         if (el.getAttribute('tabindex') === '0') score += 3;
        
#         // Skip low score elements
#         if (score < 3) return;
        
#         // ── Collect ALL attributes dynamically ──────
#         const attrs = {};
#         for (const attr of el.attributes) {
#             // Skip very long values (like base64 images)
#             if (attr.value.length < 200) {
#                 attrs[attr.name] = attr.value;
#             }
#         }
        
#         // ── Build best possible selector ─────────────
#         let cssSelector = tag;
#         let selectorQuality = 'weak';
        
#         if (attrs['data-testid']) {
#             cssSelector = `[data-testid="${attrs['data-testid']}"]`;
#             selectorQuality = 'strong';
#         } else if (attrs['id'] && !/^[a-z0-9]{15,}$/.test(attrs['id'])) {
#             cssSelector = `#${attrs['id']}`;
#             selectorQuality = 'strong';
#         } else if (attrs['name']) {
#             cssSelector = `${tag}[name="${attrs['name']}"]`;
#             selectorQuality = 'good';
#         } else if (attrs['aria-label']) {
#             cssSelector = `[aria-label="${attrs['aria-label']}"]`;
#             selectorQuality = 'good';
#         } else if (attrs['placeholder']) {
#             cssSelector = `${tag}[placeholder="${attrs['placeholder']}"]`;
#             selectorQuality = 'good';
#         } else if (attrs['type']) {
#             cssSelector = `${tag}[type="${attrs['type']}"]`;
#             selectorQuality = 'medium';
#         } else if (attrs['role']) {
#             cssSelector = `[role="${attrs['role']}"]`;
#             selectorQuality = 'medium';
#         }
        
#         // ── Build XPath ───────────────────────────────
#         const text = (el.innerText || '').trim().substring(0, 50);
#         let xpath = '';
#         if (attrs['data-testid']) {
#             xpath = `//${tag}[@data-testid="${attrs['data-testid']}"]`;
#         } else if (attrs['id'] && !/^[a-z0-9]{15,}$/.test(attrs['id'])) {
#             xpath = `//${tag}[@id="${attrs['id']}"]`;
#         } else if (attrs['name']) {
#             xpath = `//${tag}[@name="${attrs['name']}"]`;
#         } else if (attrs['aria-label']) {
#             xpath = `//${tag}[@aria-label="${attrs['aria-label']}"]`;
#         } else if (text && text.length < 40) {
#             xpath = `//${tag}[normalize-space()="${text}"]`;
#         }
        
#         // ── Classify element type ─────────────────────
#         const itype = (attrs['type'] || '').toLowerCase();
#         let elemType = tag.toUpperCase();
#         if (tag === 'input') {
#             const typeMap = {
#                 'text': 'TextInput', 'email': 'EmailInput',
#                 'password': 'PasswordInput', 'checkbox': 'Checkbox',
#                 'radio': 'RadioButton', 'submit': 'SubmitButton',
#                 'button': 'Button', 'tel': 'PhoneInput',
#                 'number': 'NumberInput', 'search': 'SearchInput',
#                 'hidden': 'HiddenInput', '': 'TextInput'
#             };
#             elemType = typeMap[itype] || 'Input';
#         } else if (tag === 'button') elemType = 'Button';
#         else if (tag === 'a')        elemType = 'Link';
#         else if (tag === 'select')   elemType = 'Dropdown';
#         else if (tag === 'textarea') elemType = 'TextArea';
#         else if (role === 'button')  elemType = 'Button';
#         else if (role === 'link')    elemType = 'Link';
#         else if (role === 'textbox') elemType = 'TextInput';
        
#         // ── Generate smart element name ───────────────
#         let name = (
#             attrs['data-testid'] ||
#             attrs['aria-label']  ||
#             attrs['name']        ||
#             attrs['id']          ||
#             attrs['placeholder'] ||
#             attrs['title']       ||
#             (text.length > 0 && text.length < 30 ? text : '') ||
#             `${tag}_${index}`
#         );
#         name = name.replace(/[^a-zA-Z0-9_\-\s]/g, '')
#                    .trim()
#                    .replace(/\s+/g, '_')
#                    .substring(0, 50);
        
#         results.push({
#             element_name:     name,
#             tag:              tag,
#             element_type:     elemType,
#             score:            score,
#             selector_quality: selectorQuality,
#             css_selector:     cssSelector,
#             xpath:            xpath,
#             attributes:       attrs,
#             visible_text:     text,
#             position: {
#                 x:      Math.round(rect.x),
#                 y:      Math.round(rect.y),
#                 width:  Math.round(rect.width),
#                 height: Math.round(rect.height)
#             }
#         });
#     });
    
#     // Sort by score (most interactive first)
#     return results.sort((a, b) => b.score - a.score);
# }
# """

# def dedupe_names(elements):
#     seen = {}
#     for el in elements:
#         n = el["element_name"] or el["tag"]
#         if not n:
#             n = "element"
#         if n in seen:
#             seen[n] += 1
#             el["element_name"] = f"{n}_{seen[n]}"
#         else:
#             seen[n] = 1
#     return elements

# def build_repo(url, title, elements):
#     parsed   = urlparse(url)
#     app_name = parsed.netloc.replace("www.","").replace(".","_")
#     screen   = parsed.path.strip("/").replace("/","_") or "home"

#     # Group dynamically by element_type
#     grouped = {}
#     for el in elements:
#         et = el["element_type"]
#         if et not in grouped:
#             grouped[et] = {}
#         grouped[et][el["element_name"]] = {
#             "id":               str(uuid.uuid4()),
#             "tag":              el["tag"],
#             "element_type":     el["element_type"],
#             "score":            el["score"],
#             "selector_quality": el["selector_quality"],
#             "css_selector":     el["css_selector"],
#             "xpath":            el["xpath"],
#             "attributes":       el["attributes"],
#             "visible_text":     el["visible_text"],
#             "position":         el["position"],
#             "captured_at":      datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         }
#     return {
#         app_name: {
#             "version":    "1.0.0",
#             "type":       "Web",
#             "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "screens": {
#                 screen: {
#                     "url":      url,
#                     "title":    title,
#                     "elements": grouped
#                 }
#             }
#         }
#     }

# def save_repo(repo, url):
#     os.makedirs(OUTPUT_DIR, exist_ok=True)
#     parsed = urlparse(url)
#     name   = parsed.netloc.replace("www.","").replace(".","_")
#     path   = os.path.join(OUTPUT_DIR, f"{name}_repository.json")
#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(repo, f, indent=4, ensure_ascii=False)
#     return path

# def print_summary(repo, path):
#     print("\n" + "="*55)
#     print("      OBJECT REPOSITORY COMPLETE")
#     print("="*55)
#     for app, data in repo.items():
#         print(f"\n  App    : {app}")
#         for screen, sd in data["screens"].items():
#             print(f"  Screen : {screen}")
#             print(f"  URL    : {sd['url']}")
#             print(f"  Title  : {sd['title']}")
#             total = 0
#             print(f"\n  Elements (by type):")
#             for etype, elems in sd["elements"].items():
#                 c = len(elems)
#                 total += c
#                 print(f"\n    [{etype}] — {c} element(s)")
#                 for en, ed in list(elems.items())[:2]:
#                     print(f"      • {en}")
#                     print(f"        css  : {ed['css_selector']}")
#                     print(f"        xpath: {ed['xpath']}")
#                     print(f"        score: {ed['score']} | quality: {ed['selector_quality']}")
#             print(f"\n  TOTAL : {total} elements")
#     print(f"\n  Saved : {path}")
#     print("="*55)

# async def generate(url):
#     print(f"\n  URL: {url}")
#     async with async_playwright() as p:
#         print("  Launching browser (Playwright)...")
#         browser = await p.chromium.launch(headless=False)
#         page    = await browser.new_page()

#         print("  Opening page...")
#         await page.goto(url, wait_until="networkidle", timeout=30000)
#         title = await page.title()
#         print(f"  Loaded : {title}")

#         print("  Scanning ALL elements dynamically...")
#         raw = await page.evaluate(DYNAMIC_SCAN_SCRIPT)
#         print(f"  Found  : {len(raw)} interactive elements")

#         elements = dedupe_names(raw)
#         repo     = build_repo(url, title, elements)
#         path     = save_repo(repo, url)
#         print_summary(repo, path)

#         await browser.close()
#         return path

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("\nUsage: python object_repo.py <URL>")
#         print("Examples:")
#         print("  python object_repo.py https://accounts.google.com/signup")
#         print("  python object_repo.py https://github.com/login")
#         print("  python object_repo.py https://amazon.com")
#         sys.exit(1)

#     asyncio.run(generate(sys.argv[1]))










"""
Universal Web Object Repository Generator
- Uses Playwright (NOT Selenium)
- Reads ALL DOM elements dynamically
- Identifies input elements automatically
- No hardcoded element lists anywhere
Usage: python object_repo.py <URL>
"""

import json, os, sys, uuid, asyncio
from datetime import datetime
from urllib.parse import urlparse
from playwright.async_api import async_playwright

OUTPUT_DIR = "repositories"


DOM_SCAN_SCRIPT = """
() => {
    const results = [];

    // Get ALL elements on page 
    const allElements = document.querySelectorAll('*');

    allElements.forEach((el, index) => {

        // Skip invisible elements
        const style = window.getComputedStyle(el);
        if (style.display === 'none'    ||
            style.visibility === 'hidden' ||
            style.opacity === '0') return;

        const rect = el.getBoundingClientRect();
        if (rect.width < 5 || rect.height < 5) return;

        const tag  = el.tagName.toLowerCase();
        const role = (el.getAttribute('role') || '').toLowerCase();
        const type = (el.getAttribute('type') || '').toLowerCase();

        // Identify if this is an INPUT element 
        
        const isInput =
            // Standard form input elements
            tag === 'input'    ||
            tag === 'textarea' ||
            tag === 'select'   ||
            tag === 'button'   ||

            // Anchor tags (clickable links)
            tag === 'a'        ||

        
            role === 'button'     ||
            role === 'textbox'    ||
            role === 'checkbox'   ||
            role === 'radio'      ||
            role === 'combobox'   ||
            role === 'listbox'    ||
            role === 'menuitem'   ||
            role === 'link'       ||
            role === 'searchbox'  ||
            role === 'spinbutton' ||

            el.getAttribute('contenteditable') === 'true' ||

            el.getAttribute('tabindex') === '0';

        // If NOT an input element---> skip
        if (!isInput) return;

        // Collect ALL attributes from DOM
        // No hardcoded attribute list
        const attributes = {};
        for (const attr of el.attributes) {
            // Skip very long values like base64 images
            if (attr.value && attr.value.length < 300) {
                attributes[attr.name] = attr.value;
            }
        }

        // Get visible text 
        const visibleText = (
            el.innerText        ||
            el.value            ||
            el.placeholder      ||
            el.getAttribute('aria-label') ||
            el.getAttribute('title') ||
            ''
        ).trim().substring(0, 100);

        // Build CSS selector
        // Priority: data-testid > id > name >
        //           aria-label > placeholder > type > role
        let cssSelector    = tag;
        let selectorQuality = 'weak';

        if (attributes['data-testid']) {
            cssSelector     = `[data-testid="${attributes['data-testid']}"]`;
            selectorQuality = 'strong';
        } else if (attributes['id'] &&
                   attributes['id'].length < 30 &&
                   !/^[a-z0-9]{15,}$/.test(attributes['id'])) {
            cssSelector     = `${tag}#${attributes['id']}`;
            selectorQuality = 'strong';
        } else if (attributes['name']) {
            cssSelector     = `${tag}[name="${attributes['name']}"]`;
            selectorQuality = 'good';
        } else if (attributes['aria-label']) {
            cssSelector     = `[aria-label="${attributes['aria-label']}"]`;
            selectorQuality = 'good';
        } else if (attributes['placeholder']) {
            cssSelector     = `${tag}[placeholder="${attributes['placeholder']}"]`;
            selectorQuality = 'good';
        } else if (attributes['type']) {
            cssSelector     = `${tag}[type="${attributes['type']}"]`;
            selectorQuality = 'medium';
        } else if (role) {
            cssSelector     = `[role="${role}"]`;
            selectorQuality = 'medium';
        }

        // Build XPath 
        let xpath = '';
        if (attributes['data-testid']) {
            xpath = `//${tag}[@data-testid="${attributes['data-testid']}"]`;
        } else if (attributes['id'] && attributes['id'].length < 30) {
            xpath = `//${tag}[@id="${attributes['id']}"]`;
        } else if (attributes['name']) {
            xpath = `//${tag}[@name="${attributes['name']}"]`;
        } else if (attributes['aria-label']) {
            xpath = `//${tag}[@aria-label="${attributes['aria-label']}"]`;
        } else if (visibleText && visibleText.length < 40) {
            xpath = `//${tag}[normalize-space()="${visibleText}"]`;
        }

        // Classify input element type
        let elemType = tag.toUpperCase();
        if (tag === 'input') {
            const typeMap = {
                'text':     'TextInput',
                'email':    'EmailInput',
                'password': 'PasswordInput',
                'checkbox': 'Checkbox',
                'radio':    'RadioButton',
                'submit':   'SubmitButton',
                'button':   'Button',
                'tel':      'PhoneInput',
                'number':   'NumberInput',
                'search':   'SearchInput',
                'hidden':   'HiddenInput',
                'file':     'FileUpload',
                'date':     'DateInput',
                '':         'TextInput'
            };
            elemType = typeMap[type] || 'Input';
        } else if (tag === 'button')   elemType = 'Button';
        else if (tag === 'a')          elemType = 'Link';
        else if (tag === 'select')     elemType = 'Dropdown';
        else if (tag === 'textarea')   elemType = 'TextArea';
        else if (role === 'button')    elemType = 'Button';
        else if (role === 'textbox')   elemType = 'TextInput';
        else if (role === 'checkbox')  elemType = 'Checkbox';
        else if (role === 'combobox')  elemType = 'Dropdown';

        // Generate element name from attributes
        // No hardcoding ---> read from DOM
        const rawName = (
            attributes['data-testid']  ||
            attributes['aria-label']   ||
            attributes['name']         ||
            attributes['id']           ||
            attributes['placeholder']  ||
            attributes['title']        ||
            (visibleText.length > 0 && visibleText.length < 30
                ? visibleText : '')    ||
            `${tag}_${index}`
        );

        const cleanName = rawName
            .replace(/[^a-zA-Z0-9_\\-\\s]/g, '')
            .trim()
            .replace(/\\s+/g, '_')
            .substring(0, 50);

        results.push({
            element_name:     cleanName || `${tag}_${index}`,
            tag:              tag,
            element_type:     elemType,
            selector_quality: selectorQuality,
            css_selector:     cssSelector,
            xpath:            xpath,
            attributes:       attributes,
            visible_text:     visibleText,
            position: {
                x:      Math.round(rect.x),
                y:      Math.round(rect.y),
                width:  Math.round(rect.width),
                height: Math.round(rect.height)
            }
        });
    });

    return results;
}
"""

def dedupe_names(elements):
    seen = {}
    for el in elements:
        n = el["element_name"] or "element"
        if n in seen:
            seen[n] += 1
            el["element_name"] = f"{n}_{seen[n]}"
        else:
            seen[n] = 1
    return elements

def build_repo(url, title, elements):
    parsed   = urlparse(url)
    app_name = parsed.netloc.replace("www.","").replace(".","_")
    screen   = parsed.path.strip("/").replace("/","_") or "home"

    grouped = {}
    for el in elements:
        et = el["element_type"]
        if et not in grouped:
            grouped[et] = {}
        grouped[et][el["element_name"]] = {
            "id":               str(uuid.uuid4()),
            "tag":              el["tag"],
            "element_type":     el["element_type"],
            "selector_quality": el["selector_quality"],
            "css_selector":     el["css_selector"],
            "xpath":            el["xpath"],
            "attributes":       el["attributes"],
            "visible_text":     el["visible_text"],
            "position":         el["position"],
            "captured_at":      datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    return {
        app_name: {
            "version":    "1.0.0",
            "type":       "Web",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "screens": {
                screen: {
                    "url":      url,
                    "title":    title,
                    "elements": grouped
                }
            }
        }
    }

def save_repo(repo, url):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    parsed = urlparse(url)
    name   = parsed.netloc.replace("www.","").replace(".","_")
    path   = os.path.join(OUTPUT_DIR, f"{name}_repository.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(repo, f, indent=4, ensure_ascii=False)
    return path

def print_summary(repo, path):
    print("\n" + "="*55)
    print("      OBJECT REPOSITORY COMPLETE")
    print("="*55)
    for app, data in repo.items():
        print(f"\n  App    : {app}")
        for screen, sd in data["screens"].items():
            print(f"  Screen : {screen}")
            print(f"  URL    : {sd['url']}")
            print(f"  Title  : {sd['title']}")
            total = 0
            print(f"\n  Input Elements Found:")
            for etype, elems in sd["elements"].items():
                c = len(elems)
                total += c
                print(f"\n    [{etype}] — {c} element(s)")
                for en, ed in list(elems.items())[:3]:
                    print(f"      • {en}")
                    print(f"        css     : {ed['css_selector']}")
                    print(f"        xpath   : {ed['xpath']}")
                    print(f"        quality : {ed['selector_quality']}")
            print(f"\n  TOTAL INPUT ELEMENTS : {total}")
    print(f"\n  Saved : {path}")
    print("="*55)

async def generate(url):
    print(f"\n  URL: {url}")
    async with async_playwright() as p:
        print("  Launching Playwright browser...")
        browser = await p.chromium.launch(headless=False)
        page    = await browser.new_page()

        print("  Opening page...")
        await page.goto(url, wait_until="networkidle", timeout=30000)

        title = await page.title()
        print(f"  Loaded : {title}")

        print("  Scanning ALL DOM elements...")
        print("  Identifying input elements...")
        raw      = await page.evaluate(DOM_SCAN_SCRIPT)
        elements = dedupe_names(raw)
        print(f"  Found  : {len(elements)} input elements")

        repo = build_repo(url, title, elements)
        path = save_repo(repo, url)
        print_summary(repo, path)

        await browser.close()
        return path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage: python object_repo.py <URL>")
        print("Examples:")
        print("  python object_repo.py https://accounts.google.com/signup")
        print("  python object_repo.py https://github.com/login")
        sys.exit(1)

    asyncio.run(generate(sys.argv[1]))