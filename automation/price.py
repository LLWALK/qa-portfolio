import json, re
from playwright.sync_api import sync_playwright

URL = "https://www.scorptec.com.au/product/graphics-cards/nvidia/116019-prime-rtx5080-16g"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(URL, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)  # give the page 3 seconds to finish loading

    price = None

    # Method 1: hidden product data that shops add for Google
    for block in page.locator('script[type="application/ld+json"]').all_text_contents():
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        for item in (data if isinstance(data, list) else [data]):
            if not isinstance(item, dict):
                continue
            offers = item.get("offers")
            if isinstance(offers, list):
                offers = offers[0]
            if isinstance(offers, dict) and offers.get("price"):
                price = offers["price"]

    # Method 2 (backup): first dollar amount visible on the page
    if price is None:
        match = re.search(r"\$\s?([\d,]+\.\d{2})", page.inner_text("body"))
        if match:
            price = match.group(1) + " (backup method - double-check this)"

    print("Product:", page.title())
    print("Price: $", price)
    browser.close()