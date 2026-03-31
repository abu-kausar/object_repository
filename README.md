# PyRPAx-Framework

PyRPAx-Framework is a lightweight Python toolkit for capturing the UI structure and visual state of web pages to support Robotic Process Automation (RPA) workflows, UI analysis, and automated element extraction. It uses Playwright for browser control, extracts structural and accessibility information about interactive elements, records screenshots, annotates them, and writes structured JSON output describing pages and controls.

This README documents the repository layout, explains the purpose of each script and module, and shows how to run the main capture flow and example scripts.

Status
------
Prototype / early-stage — functional scripts for DOM inspection, screenshot capture and annotation. Contributions, bug reports and improvements are welcome.

Quick summary
-------------
- Main capture flow: `main.py` — run a Playwright browser, observe DOM changes and network events, extract interactive elements, save JSON describing pages and controls, take screenshots and annotate them.
- Core browser control: `core/browser_manager.py` — starts Playwright and returns a page & context.
- Extraction: `extractor/` — element detection, control-type heuristics and label helpers.
- Storage: `repository/json_storage.py` — writes output JSON after de-duplication.
- Screenshot/annotation: `screenshot/` — take screenshots and draw element annotations.
- Example (Selenium): `simple_design/main.py` — simple page object usage for reference.
- Helpers and utilities: `utils/`, `common/` and additional scripts such as `dom_parsing.py`.

Repository structure
--------------------
PyRPAx-Framework/
- .github/                — CI / issue templates (if present)
- common/                 — common utilities (logger, etc.)
- core/
  - browser_manager.py    — Playwright start-up wrapper (provides page & context)
- extractor/
  - element_extractor.py  — enumerates interactive elements and captures attributes
  - control_detector.py   — heuristics to map tags/attributes to control types
  - label_utils.py        — helper to find label text for elements
- repository/
  - json_filter.py        — (de-)duplication helpers for repository data
  - json_storage.py       — persists repository JSON into output/
- screenshot/
  - screenshot_service.py — take screenshots of pages
  - draw_annotator.py     — draw boxes/annotations for discovered elements
- simple_design/
  - main.py               — short Selenium-based example using a Page Object
- dom_parsing.py          — utility script related to DOM parsing (auxiliary helpers)
- main.py                 — main capture workflow (Playwright-based)
- requirements.txt        — runtime dependencies
- env.txt                 — sample environment variables / notes
- ProjectPlan.md          — notes / project plan
- README.md               — (this file)

Files and purpose (detailed)
----------------------------

main.py
- Entry point for the Playwright capture workflow.
- Usage: `python main.py <url>`
- Behavior:
  - Starts Playwright via `core.browser_manager.BrowserManager`.
  - Instantiates the core services:
    - `ElementExtractor(repo)` — scans the page and frames, capturing attributes and element bounding boxes into `repo`.
    - `JsonStorage()` — writes filtered JSON to `output/<base_name>.json`.
    - `ScreenshotService()` — captures screenshots per screen state.
    - `DrawAnnotator(base_name, repo)` — draws annotated screenshots from extracted element metadata.
  - Injects a DOM MutationObserver into the page to detect DOM changes (with debounce) and exposes a Python callback `notify_dom_change`.
  - Registers listeners for navigation, network responses, and DOMContentLoaded to trigger extraction when relevant events occur.
  - Saves JSON and screenshots for each distinct screen state (versioned by screen key).

core/browser_manager.py
- Minimal Playwright wrapper:
  - `start()` initializes Playwright, launches Chromium (defaults to headful in this code), creates a context and a page, and returns `(page, context)`.
- Recommendation: switch to headless for automated runs or expose launch options.

extractor/element_extractor.py
- Scans a page using a list of selectors (inputs, textarea, select, button, anchors, roles, ARIA attributes, data attributes, tabindex).
- For each element it captures:
  - bounding box (position & size)
  - element metadata: tag, type, id, name, placeholder, autocomplete, title, aria-label, class, data attributes
  - label: best-effort extracted label (via `label_utils`)
  - control_type: heuristic determined by `control_detector.detect_control(...)`
  - selector: normalized selector string (helper `normalize_selector`)
- Appends unique element records to `repo["pages"][screen_name]`.

extractor/control_detector.py
- Implements heuristics to map HTML tag, `type` attribute, ARIA role, and element characteristics to a friendly `control_type` label (e.g., text input, button, link, checkbox, radio, select).
- Used by ElementExtractor to improve the semantic meaning of discovered elements.

extractor/label_utils.py
- Helps identify associated label text for an element by checking:
  - `<label for="id">` references
  - parent `<label>` containers
  - `aria-label` / `title` attributes
  - nearby text heuristics
- Returns best-guess label text for the element record.

repository/json_filter.py
- Provides functions to remove duplicate or redundant element entries from the `repo` structure before saving. This keeps the output concise and avoids repeated identical entries across captures.

repository/json_storage.py
- `JsonStorage.save(repo, base_name)`:
  - Calls `filter_duplicate_elements(repo)` to deduplicate.
  - Ensures the `output/` directory exists.
  - Writes `output/<base_name>.json` with pretty-printed JSON describing `base_url` and `pages`.
  - Prints confirmation of the saved file.

screenshot/screenshot_service.py
- Responsible for capturing screenshots of the page for each captured screen state. Called from `main.py` as `screenshot.take(page, base_name, versioned_name)`.

screenshot/draw_annotator.py
- Reads `repo` element metadata and draws bounding boxes/labels/identifiers on saved screenshots to produce annotated visual output.
- `annotator.draw_all()` will generate annotated images for inspection.

simple_design/main.py
- A short Selenium example demonstrating a Page Object pattern and how a test or automation might be structured.
- Not directly part of the Playwright capture flow but provided as a reference or alternative design example.

dom_parsing.py
- Collection of DOM parsing helpers and utilities for ancillary processing.

Requirements & setup
--------------------
- Python 3.8+ recommended.
- Install dependencies:
  ```bash
  python -m venv .venv
  source .venv/bin/activate   # macOS / Linux
  .\.venv\Scripts\activate    # Windows PowerShell / CMD
  pip install -r requirements.txt
  ```
- If Playwright is used, install the browser binaries if required:
  ```bash
  playwright install
  ```
- For Selenium example usage, install Selenium and ensure the appropriate WebDriver (e.g., chromedriver) is available on your PATH.

Running the main capture flow
-----------------------------
1. Run the capture:
   ```bash
   python main.py https://example.com
   ```
   - The script opens a browser, observes DOM/network changes, extracts elements for each discovered screen state, captures screenshots, and writes JSON to `output/<base_name>.json`.
   - Annotated screenshots are created by the draw annotator.

Example snippet (illustrative)
```python
# example.py (illustrative)
from extractor.element_extractor import ElementExtractor
from core.browser_manager import BrowserManager

browser = BrowserManager()
page, context = browser.start()

repo = {"base_url": "https://example.com", "pages": {}}
extractor = ElementExtractor(repo)

# run a manual capture
extractor.extract(page, "home")
```

Output
------
- JSON files: `output/<base_name>.json` — structured data describing `base_url` and `pages`. Each page key maps to an array of element records containing attributes, bounding boxes, labels, and a computed `control_type`.
- Screenshots: captured per screen version (name includes version suffix).
- Annotated screenshots: produced by `screenshot/draw_annotator.py` to visually inspect discovered elements.

Design notes & behavior
-----------------------
- Detection: a MutationObserver injected into the page watches for DOM changes; navigation and XHR/fetch responses also trigger extraction. Debounce logic prevents excessive firing on rapid DOM updates.
- Robustness: the extractor skips elements without bounding boxes and wraps many operations in try/except to tolerate dynamic page conditions.
- De-duplication: JSON output is cleaned by `json_filter` prior to writing.
- Browser configuration: `BrowserManager` currently launches Chromium with `headless=False`. For automated runs or CI, change this option.

Extending the project
---------------------
- Add adapters for other browsers or remote drivers.
- Enhance `control_detector` heuristics to cover complex/custom controls.
- Improve label/semantic extraction (NLP heuristics, contextual analysis).
- Add unit tests, integration tests, and CI workflows to validate extraction quality across example pages.

Contributing
------------
- Fork the repository, create a feature branch, add tests and documentation, and open a pull request.
- Follow consistent coding style and include a short description of changes in your PR.

License
-------
- Add a LICENSE file to the repository (e.g., MIT, Apache-2.0) and update this README accordingly.

Maintainer
----------
- Repository owner / contact: alaminkawsar

Acknowledgements
----------------
- Prototype inspired by common RPA, UI testing and accessibility tooling patterns (Playwright, Selenium, accessibility heuristics).
