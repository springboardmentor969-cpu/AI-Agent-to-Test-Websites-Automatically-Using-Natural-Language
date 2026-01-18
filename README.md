# AI Web Testing Agent - Enhanced Edition 🤖🌃🦾

Minimalist, powerful, and ultra-futuristic autonomous web testing engine with **AI-powered instruction understanding** and **advanced execution capabilities**. Built for reliability, precision, and high-impact visual reporting.

![Version](https://img.shields.io/badge/version-2.0--enhanced-blueviolet?style=for-the-badge)
![UI](https://img.shields.io/badge/UI-Vibrant_Futurism-darkblue?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Grok_(xAI)_Enhanced-neon?style=for-the-badge)

## 🌟 What's New in Enhanced Edition

### 🧠 AI-Powered Instruction Parsing
- **Natural Language Understanding**: Write test instructions in plain English
- **Complex Action Support**: Handle multi-step workflows, conditionals, and data extraction
- **Variable Management**: Extract and reuse data across test steps
- **Intelligent Fallback**: Automatic fallback to pattern matching if AI is unavailable

### ⚡ Advanced Execution Capabilities
- **Smart Wait Strategies**: AJAX detection, animation waiting, network idle detection
- **Iframe Support**: Seamlessly interact with iframe content
- **File Operations**: Upload and download files automatically
- **Multi-Tab Management**: Handle multiple browser tabs and windows
- **Complex Interactions**: Hover, drag-drop, keyboard shortcuts, scrolling
- **Data Extraction**: Extract text, attributes, and table data from pages

### 🔧 Intelligent AI Healing
- **Enhanced Context**: Provides page URL, title, and surrounding HTML to AI
- **Semantic Analysis**: Fallback selector generation using DOM analysis
- **Selector Caching**: Reuses successful healings to reduce API calls
- **Multiple Strategies**: Tries heuristics, AI, and semantic analysis in sequence
- **Healing Statistics**: Track healing success rates and cache performance

### 🛡️ Robust Error Handling
- **Error Categorization**: Automatically categorizes errors (timeout, element not found, etc.)
- **Recovery Strategies**: Suggests specific fixes for each error type
- **Exponential Backoff**: Smart retry logic with increasing wait times
- **Detailed Reporting**: Error reports with context and recovery suggestions

### 📊 Enhanced Reporting
- **Console Logs**: Capture browser console output
- **Healing Stats**: View AI healing performance metrics
- **Variable Tracking**: See extracted variables and their values
- **Step Screenshots**: Optional screenshot capture at each step

### 📚 Documentation

- **[README.md](file:///e:/aiwebtestingagent/README.md)** - Complete guide
- **[EXAMPLES.md](file:///e:/aiwebtestingagent/docs/EXAMPLES.md)** - Test examples
- **[ENHANCEMENT_SUMMARY.md](file:///e:/aiwebtestingagent/docs/ENHANCEMENT_SUMMARY.md)** - What's new

## 🌌 Key Features

- **"Unbreakable" AI Execution**: Combines local heuristics with **Grok (xAI)** intelligence to heal broken selectors in real-time
- **Cyber-Noir Dashboard**: A cinematic, high-fidelity UI with animated backgrounds and tactical display modules
- **Direct Reporting**: Instant visibility of HTML audit reports with tiled screenshots and integrated video playback
- **Professional Exports**: Generate and download one-click **PDF and HTML** audit reports with embedded evidence
- **Windows Optimized**: Built-in support for Windows asyncio policies to ensure zero execution errors
- **Advanced Settings**: Configure timeouts, retries, AI parsing, and screenshot options

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- A valid **Grok (xAI) API Key** (Set in `.env`)

### 2. Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd aiwebtestingagent

# Create and activate virtual environment
python -m venv projenv310
# Windows:
projenv310\\Scripts\\activate
# Linux/Mac:
source projenv310/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
# Grok API Key (Get yours at https://console.x.ai/)
GROK_API_KEY=your_key_here
```

### 4. Running the App
```bash
streamlit run ui/app.py
```

The app will open in your browser at `http://localhost:8501`

## 📝 Writing Test Instructions

### Basic Examples

**Simple Navigation and Search:**
```
Go to https://google.com
Type "AI testing tools" in the search box
Press Enter
Verify "results" appears on the page
```

**Form Filling:**
```
Navigate to https://example.com/signup
Type "john@example.com" in the email field
Type "SecurePass123" in the password field
Click the "Sign Up" button
Wait for "Welcome" text
```

### Advanced Examples

**Data Extraction:**
```
Go to https://example.com/products
Extract the price as {product_price}
Extract the title as {product_name}
Click "Add to Cart"
```

**Multi-Step Workflow:**
```
Open https://example.com
Click "Login" button
Type "user@test.com" in email
Type "password123" in password
Click "Submit"
Wait for element "#dashboard"
Verify "Welcome back" text
```

**File Upload:**
```
Navigate to https://example.com/upload
Upload "C:\\Users\\Documents\\test.pdf" to file input
Click "Upload" button
Wait for "Upload successful" text
```

## 🎯 Supported Actions

| Action | Description | Example |
|--------|-------------|---------|
| `goto` | Navigate to URL | `Go to https://google.com` |
| `click` | Click element | `Click the login button` |
| `type` | Type text | `Type "hello" in search box` |
| `hover` | Hover over element | `Hover over the menu` |
| `select` | Select dropdown option | `Select "United States" from country` |
| `scroll` | Scroll page | `Scroll down 500px` |
| `wait` | Wait for condition | `Wait for "loading" to disappear` |
| `extract` | Extract data | `Extract price as {price}` |
| `upload` | Upload file | `Upload "file.pdf"` |
| `press_key` | Press keyboard key | `Press Enter` |
| `assert_text` | Verify text exists | `Verify "Success" appears` |
| `assert_element` | Verify element exists | `Check login button exists` |

## ⚙️ Advanced Settings

Access advanced settings in the UI by expanding the "⚙️ ADVANCED SETTINGS" panel:

- **🤖 AI-Powered Parsing**: Enable/disable AI instruction understanding
- **Timeout (ms)**: Set maximum wait time for actions (default: 10000ms)
- **📸 Screenshot Each Step**: Capture screenshots after every action
- **Max Retries**: Number of retry attempts for failed actions (default: 3)

## 🛠️ Tech Stack

- **Engine**: LangGraph, Playwright
- **AI**: Grok (xAI) via direct API integration
- **Interface**: Streamlit (with Custom Cyberpunk CSS)
- **Reporting**: FPDF2, Jinja2
- **Parsing**: BeautifulSoup4, Custom NLP
- **Configuration**: Python-dotenv, Pydantic

## 🛡️ Architecture

The enhanced agent uses a **State-Based Batch Execution** model with intelligent error handling:

1. **AI-Powered Instruction Parsing**: Converts natural language to structured actions using Grok AI
2. **Enhanced Execution**: Executes actions with smart waits, healing, and retry logic
3. **Intelligent AI Healing**: Multi-strategy selector healing with caching
4. **Error Handling**: Categorizes errors and suggests recovery strategies
5. **Comprehensive Reporting**: Generates detailed reports with visual evidence

### Component Architecture

```
agent/
├── config.py                 # Centralized configuration
├── enhanced_parser.py        # AI-powered instruction parser
├── enhanced_executor.py      # Advanced action executor
├── enhanced_graph.py         # LangGraph workflow
├── ai_selector.py           # Enhanced AI healing
├── selector_cache.py        # Healing cache system
├── error_handler.py         # Error categorization & recovery
├── smart_waits.py           # Advanced wait strategies
├── advanced_actions.py      # Complex interaction handlers
├── reporter.py              # Report generation
└── parallel_executor.py     # Batch execution
```

## 📊 Configuration Options

Edit `agent/config.py` to customize:

```python
# Timeout Configuration
DEFAULT_TIMEOUT = 10000
NAVIGATION_TIMEOUT = 30000
ELEMENT_TIMEOUT = 5000

# Retry Configuration
MAX_RETRIES = 3
EXPONENTIAL_BACKOFF = True

# AI Healing
AI_HEALING_ENABLED = True
SELECTOR_CACHE_ENABLED = True

# Screenshots
SCREENSHOT_ON_ERROR = True
SCREENSHOT_EACH_STEP = False

# Browser
HEADLESS_MODE = True
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 720
```

## 🔍 Troubleshooting

### Common Issues

**1. AI Parsing Not Working**
- Verify `GROK_API_KEY` is set in `.env`
- Check API key is valid at https://console.x.ai/
- Fallback to pattern matching will activate automatically

**2. Selector Healing Fails**
- Check internet connection
- Verify Grok API quota
- Review selector cache at `tests/selector_cache.json`

**3. Timeout Errors**
- Increase timeout in Advanced Settings
- Check if page is slow to load
- Verify network connectivity

**4. Import Errors**
- Run `pip install -r requirements.txt`
- Ensure virtual environment is activated
- Check Python version (3.10+ required)

## 📈 Performance Tips

1. **Enable Selector Caching**: Reduces API calls and improves speed
2. **Use Headless Mode**: Faster execution without browser UI
3. **Optimize Timeouts**: Set appropriate timeouts for your use case
4. **Disable Step Screenshots**: Only enable when debugging
5. **Batch Similar Tests**: Run related tests together for efficiency

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Grok (xAI)** for AI-powered selector healing and instruction parsing
- **Playwright** for reliable browser automation
- **LangGraph** for workflow orchestration
- **Streamlit** for the beautiful UI framework

---

Built with ❤️ for the future of automated testing. 🚀🤖🏁

**Version 2.0 - Enhanced Edition**
*Now with AI-powered understanding and advanced execution capabilities*
