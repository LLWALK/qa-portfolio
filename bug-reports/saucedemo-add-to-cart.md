# Cart buttons broken for every product (problem_user)

**Site:** saucedemo.com (practice site)
**Found:** 26 Nov 2026
**Severity:** High (customers cannot reliably buy or manage products)
**Reproducibility:** 100%, confirmed by automated tests

## Summary
For `problem_user`, every product has a broken cart button:
- 3 products can never be **added** to the cart
- The other 3 can be added but never **removed**

No product works fully in both directions, which suggests one shared
underlying defect rather than six separate ones.

| Product | Add to cart | Remove |
|---|---|---|
| Sauce Labs Backpack | ✅ | ❌ |
| Sauce Labs Bike Light | ✅ | ❌ |
| Sauce Labs Onesie | ✅ | ❌ |
| Sauce Labs Bolt T-Shirt | ❌ | n/a |
| Sauce Labs Fleece Jacket | ❌ | n/a |
| Test.allTheThings() T-Shirt (Red) | ❌ | n/a |

## Bug 1: "Add to cart" does nothing for 3 products

### Steps to reproduce
1. Log in as `problem_user` / `secret_sauce`
2. On the Products page, click "Add to cart" on every product

### Expected
Every product is added and its button changes to "Remove"

### Actual
Bolt T-Shirt, Fleece Jacket and Test.allTheThings() T-Shirt are never added,
and their buttons stay "Add to cart".

The other 3 work, so at first it looks like a "3 item limit". Automated
testing showed it's specific products that fail.

## Bug 2: "Remove" does nothing for the other 3 products

### Steps to reproduce
1. Log in as `problem_user` / `secret_sauce`
2. Click "Add to cart" on the Backpack, Bike Light and Onesie
3. Click "Remove" on each of them

### Expected
Each product is removed and its button changes back to "Add to cart"

### Actual
The products stay in the cart and their buttons stay "Remove".

## Control
All 6 products add and remove correctly for `standard_user`.

## Automated tests
`automation/test_saucedemo.py`
- `test_every_item_can_be_added_to_cart`: fails for problem_user (Bug 1)
- `test_every_item_can_be_removed_from_cart`: fails for problem_user (Bug 2)

Both tests pass for standard_user.
