# 🚀 AI-Powered Testing Agent - Enhanced E-Commerce Features

## ✨ What's New?

Your AI Testing Agent can now **search products, view details, and add items to cart** on Amazon!

## 🎯 Quick Start

### Simple Test Example
```
Go to https://www.amazon.in/
Type "Iphone pro max" in search
Select first product
View details
Add to cart
```

### How to Run

1. **Start the application:**
   ```bash
   streamlit run ui/app.py
   ```

2. **Enter your test instructions** in the text area

3. **Click "RUN NOW"** to execute the test

4. **View results** in the "VIEW RESULTS" tab with:
   - 📊 Success metrics
   - 📸 Screenshots (product details & cart confirmation)
   - 🎥 Full video recording
   - 📋 Detailed step-by-step logs
   - 📥 Downloadable HTML/PDF reports

## 🔧 New Commands

### 🛍️ Select Product
Choose a specific product from search results:
- `select first product` - Click the 1st result
- `select second product` - Click the 2nd result  
- `select third product` - Click the 3rd result
- `choose product 2` - Click product at position 2

### 👁️ View Details
Load and verify product details page:
- `view details`
- `see product details`
- `open details`
- `show information`

**Automatic features:**
- ✅ Waits for page to fully load
- 📸 Captures full-page screenshot of product
- 🔍 Verifies product title is visible

### 🛒 Add to Cart
Add the current product to your shopping cart:
- `add to cart`
- `put in cart`
- `add to basket`

**Automatic features:**
- ✅ Finds and clicks "Add to Cart" button
- ⏱️ Waits for cart confirmation
- 📸 Captures screenshot after adding

## 📝 More Examples

### Example 1: Test Different Positions
```
Go to https://www.amazon.in/
Type "wireless headphones" in search
Select second product
View details
Add to cart
```

### Example 2: Just Browse
```
Go to https://www.amazon.in/
Type "laptop" in search
Select third product
View details
```

### Example 3: Quick Add
```
Go to https://www.amazon.in/
Type "phone case" in search
Select first product
Add to cart
```

## 🎨 Features

### Intelligent Selectors
- Multiple fallback strategies for finding products
- Works with Amazon's dynamic page structure
- Automatic retry on failures

### Visual Evidence
- **Product Details Screenshot**: Full-page capture of product information
- **Cart Confirmation Screenshot**: Proof that item was added
- **Video Recording**: Complete test execution video
- **Error Screenshots**: Captured when issues occur

### Detailed Reporting
- Step-by-step execution logs
- Color-coded status indicators (✅ success, ⚠️ warning, ❌ error)
- HTML and PDF report generation
- Embedded screenshots in reports

### Smart Waiting
- Automatically waits for DOM to be ready
- Waits for network requests to complete
- Handles page transitions smoothly

## 🔍 How It Works

1. **Parser** (`parser.py`):
   - Converts natural language to actions
   - Parses position numbers (first, second, 1st, 2nd, etc.)
   - Detects product selection, view details, and add to cart commands

2. **Executor** (`executor.py`):
   - Executes actions using Playwright
   - Uses Amazon-specific selectors
   - Multiple fallback strategies
   - Captures screenshots and videos
   - Detailed logging

3. **UI** (`ui/app.py`):
   - Beautiful cyberpunk-themed interface
   - Real-time progress updates
   - Visual results dashboard
   - Download reports

## 📂 Output Files

All test artifacts are saved:
- 📸 Screenshots: `tests/screenshots/`
- 🎥 Videos: `tests/videos/`
- 📄 Reports: `tests/reports/`

## 🎓 Tips

1. **Wait for Results**: The search takes a moment to load - the agent handles this automatically

2. **Product Positions**: Amazon shows sponsored results first, so "first product" might be a sponsored ad

3. **Screenshots**: Check the screenshots in the results tab to verify correct product was selected

4. **Videos**: Download the video to see the entire test execution

5. **Error Handling**: If a selector fails, the agent tries multiple alternatives automatically

## 🐛 Troubleshooting

**Product not found?**
- Ensure search results are showing
- Try a different position (second or third product)
- Check if Amazon changed their page structure

**Add to cart failed?**
- Some products require size/color selection first
- Check the screenshot to see what happened
- View the detailed logs for error messages

**Slow execution?**
- Amazon has rate limiting - this is normal
- The agent waits for network idle before proceeding
- Videos show real-time execution speed

## 📚 Documentation

- `ECOMMERCE_FEATURES.md` - Technical details and implementation
- `example_amazon_test.md` - More test examples
- `amazon_test_examples.py` - Python script with example tests

## 🚀 Next Steps

Try these advanced workflows:
1. Search multiple products and compare
2. Test different search terms
3. Verify product details (price, ratings, etc.)
4. Test cart functionality end-to-end

---

**Happy Testing! 🎉**

For questions or issues, check the logs in the results tab or review the screenshots/video.
