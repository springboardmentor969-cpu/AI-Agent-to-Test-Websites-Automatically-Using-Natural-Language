# Example Test Instructions for AI Web Testing Agent

## Basic Tests

### Test 1: Simple Navigation and Search
```
Go to https://www.google.com
Type "AI testing automation" in the search box
Press Enter
Verify "results" appears on the page
```

### Test 2: GitHub Repository Search
```
Navigate to https://github.com
Click the search box
Type "playwright python"
Press Enter
Wait for search results
Verify "repositories" text
```

## Intermediate Tests

### Test 3: Form Interaction
```
Go to https://www.w3schools.com/html/html_forms.asp
Scroll down 300px
Type "John Doe" in the first name field
Type "Doe" in the last name field
Click the Submit button
```

### Test 4: Data Extraction
```
Open https://www.example.com
Extract the page title as {page_title}
Extract the main heading as {heading}
Verify "Example Domain" text
```

## Advanced Tests

### Test 5: Multi-Step Workflow
```
Navigate to https://www.wikipedia.org
Click the search input
Type "Artificial Intelligence"
Press Enter
Wait for page to load
Verify "Artificial intelligence" heading
Scroll down 500px
Extract the first paragraph as {intro}
```

### Test 6: Complex Interaction
```
Go to https://www.google.com
Type "weather forecast" in search
Press Enter
Wait for results
Hover over the first result
Click the first result
Wait for "weather" text
```

## Real-World Scenarios

### Test 7: E-commerce Product Search
```
Navigate to https://www.amazon.com
Type "wireless mouse" in the search box
Press Enter
Wait for search results
Extract the first product title as {product_name}
Extract the first product price as {product_price}
Verify "results" appears
```

### Test 8: Documentation Navigation
```
Go to https://playwright.dev
Click "Docs" link
Wait for documentation page
Verify "Getting started" text
Scroll down 400px
Click "Installation" link
Verify "install" text appears
```

## Tips for Writing Test Instructions

1. **Be Specific**: Use clear, descriptive language
   - Good: "Click the blue Login button"
   - Better: "Click Login button"
   - Best: "Click button:has-text('Login')"

2. **Use Variables**: Extract and reuse data
   ```
   Extract price as {price}
   Verify {price} is displayed
   ```

3. **Add Waits**: For dynamic content
   ```
   Click Submit
   Wait for "Success" text
   ```

4. **Verify Results**: Always validate outcomes
   ```
   Click Login
   Verify "Welcome" appears
   ```

5. **Handle Errors**: Use retry-friendly instructions
   ```
   Wait for element to appear
   Click the element
   ```

## Advanced Features

### Using AI Parsing (Recommended)
Enable "🤖 AI-Powered Parsing" in Advanced Settings for:
- Natural language understanding
- Complex instruction interpretation
- Automatic selector generation
- Context-aware parsing

### Custom Timeouts
Adjust timeout in Advanced Settings for:
- Slow-loading pages: 30000ms (30s)
- Fast interactions: 5000ms (5s)
- Default: 10000ms (10s)

### Screenshot Options
Enable "📸 Screenshot Each Step" to:
- Debug test failures
- Document test execution
- Create visual reports

### Retry Configuration
Set "Max Retries" based on:
- Stable sites: 1-2 retries
- Dynamic sites: 3-4 retries
- Flaky sites: 4-5 retries

## Troubleshooting

### If Tests Fail
1. Check if AI Parsing is enabled
2. Increase timeout in Advanced Settings
3. Add explicit wait statements
4. Verify selectors are correct
5. Check browser console logs in results

### If Selectors Don't Work
1. AI Healing will attempt to fix automatically
2. Use more specific selectors
3. Try text-based selectors: `button:has-text('Click Me')`
4. Check if element is in iframe
5. Wait for element to appear before interacting

### If Page Doesn't Load
1. Verify URL is correct and accessible
2. Increase navigation timeout
3. Check internet connection
4. Try in headed mode (disable Background Mode)
5. Check for redirects or popups

## Best Practices

1. **Start Simple**: Begin with basic navigation and clicks
2. **Add Complexity Gradually**: Build up to advanced workflows
3. **Use Descriptive Names**: Make instructions readable
4. **Verify Each Step**: Add assertions to validate state
5. **Handle Dynamic Content**: Use waits for AJAX/lazy loading
6. **Extract Important Data**: Save values for later use
7. **Test in Headed Mode First**: Debug visually before automation
8. **Review Logs**: Check execution logs for insights
9. **Optimize Timeouts**: Balance speed and reliability
10. **Cache Selectors**: Let AI healing build cache over time
