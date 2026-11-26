# Product page title repeats the store name

**Site:** scorptec.com.au
**Found:** 24 Nov 2026 · **Retested:** 26 Nov 2026
**Severity:** Low (cosmetic) · **Reproducibility:** 6/6 runs

## Steps to reproduce
1. Open any product page, e.g. the ASUS PRIME RTX 5080 16GB
2. Look at the browser tab title

## Expected
ASUS PRIME GeForce RTX 5080 16GB | Scorptec Computers

## Actual
ASUS PRIME GeForce RTX 5080 16GB | Scorptec Computers | Scorptec Computers

## Impact
- Cosmetic for shoppers (tab title, bookmarks, search results)
- The doubled title is also sent to Bing Ads tracking, so their ad analytics data contains the wrong page title

## How it was found
First spotted with price.py, then confirmed automatically with bug_hunter.py across 6 runs.
