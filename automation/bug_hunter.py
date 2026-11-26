import sys
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "https://www.scorptec.com.au"
problems = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Listen for errors while the page loads
    page.on("console", lambda msg: problems.append(f"Console error: {msg.text}")
            if msg.type == "error" else None)
    page.on("response", lambda r: problems.append(f"Failed request ({r.status}): {r.url}")
            if r.status >= 400 else None)

    page.goto(URL, wait_until="load")
    page.wait_for_timeout(3000)

    # Check 1: repeated parts in the page title (your Scorptec bug!)
    parts = [x.strip() for x in page.title().split("|")]
    if len(parts) != len(set(parts)):
        problems.append(f"Title repeats itself: {page.title()}")

    # Check 2: images that failed to load
    broken = page.eval_on_selector_all(
    	"img", "imgs => imgs.filter(i => i.complete && i.naturalWidth === 0 && i.offsetWidth > 1).map(i => i.src)")
    for src in broken:
        problems.append(f"Broken image: {src}")

    # Check 3: images with no alt text (bad for screen-reader users)
    missing_alt = page.locator("img:not([alt])").count()
    if missing_alt:
        problems.append(f"{missing_alt} image(s) missing alt text")

    browser.close()

print(f"Checked: {URL}\n")
if problems:
    for p_ in problems:
        print("-", p_)
else:
    print("No problems found.")