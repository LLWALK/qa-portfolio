import csv, json
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "https://www.scorptec.com.au/product/graphics-cards/nvidia/116019-prime-rtx5080-16g"
HISTORY = Path("prices.csv")


def get_price(page):
    """Read the price from the shop's hidden product data."""
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
                offers = offers[0] if offers else None
            if isinstance(offers, dict) and offers.get("price"):
                return float(offers["price"])
    return None


def last_saved_price():
    """Get the most recent price from prices.csv, if there is one."""
    if not HISTORY.exists():
        return None
    with HISTORY.open() as f:
        rows = list(csv.reader(f))
    return float(rows[-1][1]) if rows else None


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # runs invisibly this time
    page = browser.new_page()
    page.goto(URL, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    price = get_price(page)
    browser.close()

if price is None:
    print("Couldn't find a price - the page may have changed.")
else:
    previous = last_saved_price()
    with HISTORY.open("a", newline="") as f:
        csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), price])

    if previous is None:
        print(f"First check: ${price:,.2f} (saved)")
    elif price < previous:
        print(f"Price DROPPED: ${previous:,.2f} -> ${price:,.2f}")
    elif price > previous:
        print(f"Price went UP: ${previous:,.2f} -> ${price:,.2f}")
    else:
        print(f"No change: ${price:,.2f}")