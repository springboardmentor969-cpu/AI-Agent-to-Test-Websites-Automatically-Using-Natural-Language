"""
Example Test Script for Amazon Product Search and Add to Cart

This demonstrates the new e-commerce testing capabilities.
You can run this through the Streamlit UI or modify it for programmatic testing.
"""

# Example 1: Quick Test - Search and Add First Product
example1 = """
Go to https://www.amazon.in/
Type "Iphone 15 pro max" in search
Select first product
View details
Add to cart
"""

# Example 2: Select Second Product
example2 = """
Go to https://www.amazon.in/
Type "wireless earbuds" in search
Select second product
View details
Add to cart
"""

# Example 3: Select Third Product
example3 = """
Go to https://www.amazon.in/
Type "laptop backpack" in search
Select third product
View details
"""

# Example 4: Just Search and Check Results
example4 = """
Go to https://www.amazon.in/
Type "gaming mouse" in search
"""

# Example 5: Multiple Steps
example5 = """
Go to https://www.amazon.in/
Type "smartwatch" in search
Select first product
View details
Add to cart
"""

if __name__ == "__main__":
    print("Amazon E-Commerce Testing Examples")
    print("=" * 50)
    print("\nCopy and paste any of these examples into the Streamlit UI:")
    print("\n--- Example 1: iPhone Pro Max ---")
    print(example1)
    print("\n--- Example 2: Wireless Earbuds ---")
    print(example2)
    print("\n--- Example 3: Laptop Backpack ---")
    print(example3)
    print("\n--- Example 4: Gaming Mouse ---")
    print(example4)
    print("\n--- Example 5: Smartwatch ---")
    print(example5)
    
    print("\n" + "=" * 50)
    print("\nTo run the tests:")
    print("1. Start the UI: streamlit run ui/app.py")
    print("2. Paste one of the examples above")
    print("3. Click 'RUN NOW'")
    print("4. View results in the 'VIEW RESULTS' tab")
