# Amazon Product Testing Examples

This document shows how to use the AI Testing Agent to test Amazon e-commerce workflows.

## Example 1: Search and Select First Product

```
Go to https://www.amazon.in/
Type "Iphone pro max" in search
Select first product
View details
Add to cart
```

## Example 2: Select Specific Product Position

```
Go to https://www.amazon.in/
Type "laptop" in search
Select second product
View details
```

## Example 3: Search, View, and Add Multiple Products

```
Go to https://www.amazon.in/
Type "wireless headphones" in search
Select third product
View details
Add to cart
```

## Supported Instructions

### Product Selection
- `select first product` - Selects the 1st search result
- `select second product` - Selects the 2nd search result
- `select third product` - Selects the 3rd search result
- `choose product 1` - Selects product at position 1
- `pick item 2` - Selects item at position 2

### View Details
- `view details`
- `see details`
- `open details`
- `show information`

### Add to Cart
- `add to cart`
- `put in cart`
- `add to basket`

## Complete Workflow Example

Copy and paste this into the testing agent:

```
Go to https://www.amazon.in/
Type "Iphone 15 pro max" in search
Select first product
View details
Add to cart
```

## Tips

1. **Wait for Search Results**: The agent automatically waits for the page to load and network to be idle
2. **Screenshots**: Product details and cart confirmations are automatically captured
3. **Fallback Logic**: If one selector fails, the agent tries alternative methods
4. **Position Index**: You can use 1st, 2nd, 3rd or numeric positions
