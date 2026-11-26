# "Add to cart" does nothing for 3 of 6 products (problem_user)

**Site:** saucedemo.com (practice site)
**Found:** 26 Nov 2026
**Severity:** High (customers cannot buy these products)
**Reproducibility:** 100%, confirmed by automated test

## Steps to reproduce
1. Log in as `problem_user` / `secret_sauce`
2. On the Products page, click "Add to cart" on every product

## Expected
Every product is added and its button changes to "Remove"

## Actual
These products are never added and their buttons stay "Add to cart":
- Sauce Labs Bolt T-Shirt
- Sauce Labs Fleece Jacket
- Test.allTheThings() T-Shirt (Red)

The other 3 products work, so it first looks like a "3 item limit", but the
automated test shows it's specific products that fail.

## Control
All 6 products work correctly for `standard_user`.

## Automated test
`automation/test_saucedemo.py` → `test_every_item_can_be_added_to_cart`
