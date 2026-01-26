# 🤖 AI Web Testing Agent

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Playwright](https://img.shields.io/badge/Playwright-Latest-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**An intelligent AI-powered agent that performs automated end-to-end (E2E) testing on web applications using natural language instructions.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Examples](#-examples) • [Architecture](#-architecture)

</div>

---

## 🎯 Overview

This project implements an intelligent agent capable of performing automated web testing using **natural language commands**. Simply describe what you want to test, and the AI agent will:

1. **Interpret** your natural language instructions
2. **Generate** executable Playwright test scripts
3. **Execute** tests in a headless browser
4. **Produce** detailed test reports with screenshots and videos

No more writing complex test scripts manually - just describe what you want to test in plain English!

---

## ✨ Features

### 🌐 Multi-Site Support
- **Amazon** - Search products, add to cart, navigate listings
- **Instagram** - Login, logout, navigate feed
- **Google Maps** - Get directions to any location
- **Google Forms** - Auto-fill and submit forms
- **Generic Websites** - Works with any website

### 🧠 Smart Automation
- **Natural Language Processing** - Understands plain English commands
- **Self-Healing Selectors** - Automatically recovers from selector failures
- **Site Detection** - Adapts behavior based on detected website
- **Smart Waits** - Intelligent DOM and network state detection

### 📊 Comprehensive Reporting
- **Screenshots** - Captures every step automatically
- **Video Recording** - Full test session recordings
- **Detailed Logs** - Step-by-step execution logs
- **HTML/JSON/PDF Reports** - Multiple export formats

### 🎨 Modern UI
- **Cyberpunk Theme** - Stunning orange industrial design
- **Real-time Logs** - Watch test execution live
- **Interactive Controls** - Easy-to-use interface

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/ai-web-testing-agent.git
cd ai-web-testing-agent
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Playwright Browsers
```bash
playwright install chromium
```

### Step 5: Set Up Environment Variables (Optional)
```bash
cp .env.example .env
# Edit .env and add your API keys if using AI selector healing
```

### Step 6: Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 📖 Usage

### Basic Syntax
```
Go to [URL] then [action1] then [action2] then ...
```

### Supported Actions

| Action | Syntax | Example |
|--------|--------|---------|
| **Navigate** | `go to [URL]` | `go to https://amazon.in` |
| **Search** | `search for '[text]'` | `search for 'iPhone 15'` |
| **Click** | `click [element]` | `click submit button` |
| **Type** | `type "[text]" in [field]` | `type "hello" in email` |
| **Login** | `login with "[user]" "[pass]"` | `login with "user@email.com" "pass123"` |
| **Logout** | `logout` | `logout` |
| **Add to Cart** | `add to cart` | `add to cart` |
| **Select Product** | `select [nth] product` | `select first product` |
| **Get Directions** | `get directions to [place]` | `get directions to Bangalore Palace` |
| **Fill Form** | `fill form` | `fill form` |
| **Wait** | `wait [n] seconds` | `wait 5 seconds` |
| **Scroll** | `scroll [direction]` | `scroll down` |
| **Screenshot** | `take screenshot` | `take screenshot` |
| **Verify** | `verify "[text]"` | `verify "Success"` |

---

## 💡 Examples

### 🛒 Amazon Shopping
```
Go to https://www.amazon.in then search for 'iPhone 15 Pro' then add to cart
```

### 📸 Instagram Login
```
Go to https://www.instagram.com then login with "your_username" "your_password"
```

### 🗺️ Google Maps Directions
```
Get directions to Lalbagh Botanical Garden Bangalore
```

### 🔍 Google Search
```
Go to https://www.google.com then search for 'AI testing automation'
```

### 📝 Form Filling
```
Go to https://docs.google.com/forms/d/your-form-id then fill form
```

### 🔗 Multi-Step Workflow
```
Go to https://www.amazon.in then search for 'laptop' then select first product then add to cart then take screenshot
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
│                    (Streamlit - Cyberpunk UI)                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Instruction Parser                           │
│              (Natural Language → Actions)                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Executor Engine                           │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│    │   Amazon     │  │  Instagram   │  │ Google Maps  │        │
│    │   Handler    │  │   Handler    │  │   Handler    │        │
│    └──────────────┘  └──────────────┘  └──────────────┘        │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│    │Google Forms  │  │   Generic    │  │  AI Healer   │        │
│    │   Handler    │  │   Handler    │  │  (Fallback)  │        │
│    └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Playwright Browser                          │
│                   (Headless Chrome/Chromium)                     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Reporter Module                             │
│         (Screenshots, Videos, HTML/JSON/PDF Reports)             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
ai_web_tester/
├── app.py                      # Streamlit UI (Cyberpunk Theme)
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
│
├── agent/
│   ├── __init__.py
│   ├── parser.py              # Natural language parser
│   ├── executor.py            # Test execution engine
│   ├── reporter.py            # Report generation
│   ├── ai_selector.py         # AI-powered selector healing
│   ├── smart_waits.py         # Intelligent wait strategies
│   ├── graph.py               # LangGraph workflow
│   ├── graph_batch.py         # Batch execution support
│   ├── code_generator.py      # Dynamic code generation
│   └── parallel_executor.py   # Parallel test execution
│
└── tests/
    ├── screenshots/           # Test screenshots
    └── videos/                # Test recordings
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.9+** | Core programming language |
| **Playwright** | Browser automation |
| **Streamlit** | Web UI framework |
| **LangGraph** | Agent workflow orchestration |
| **LangChain** | LLM integration |

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Optional: For AI-powered selector healing
GOOGLE_API_KEY=your_google_api_key
XAI_API_KEY=your_xai_api_key

# Browser settings
HEADLESS=true
TIMEOUT=30000
```

### Settings in UI

- **Headless Mode**: Run browser invisibly (faster)
- **Timeout**: Maximum wait time for elements
- **Video Recording**: Enable/disable test recordings

---

## 🎨 UI Themes

The application features a stunning **Cyberpunk Industrial** theme with:
- 🟠 Orange and amber color scheme
- ⚡ Animated backgrounds
- 🔶 Hexagonal patterns
- ⚠️ Warning stripe aesthetics
- 💀 Military/tech terminology

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/ai-web-testing-agent.git

# Install dev dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest

# Format code
black .
```

---

## 📋 Roadmap

- [x] Amazon support (search, add to cart)
- [x] Instagram login/logout
- [x] Google Maps directions
- [x] Google Forms filling
- [x] Screenshot capture
- [x] Video recording
- [x] Cyberpunk UI theme
- [x] Self-healing selectors
- [ ] Facebook support
- [ ] Twitter/X support
- [ ] LinkedIn support
- [ ] API endpoint for CI/CD integration
- [ ] Docker containerization
- [ ] Cloud deployment (AWS/GCP)
- [ ] Mobile browser testing
- [ ] Parallel test execution
- [ ] Test scheduling
- [ ] Slack/Discord notifications

---

## ❓ FAQ

### Q: Does it work with any website?
**A:** Yes! While it has optimized handlers for Amazon, Instagram, Google Maps, and Forms, it works with any website using generic selectors.

### Q: Is it free to use?
**A:** Yes, the core functionality is completely free. AI-powered selector healing requires API keys (optional).

### Q: Can I run it in CI/CD pipelines?
**A:** Yes! Run with `headless=True` for CI/CD environments. API endpoint support coming soon.

### Q: Does it support mobile testing?
**A:** Currently supports desktop browsers. Mobile emulation is on the roadmap.

### Q: What if a selector fails?
**A:** The agent has self-healing capabilities with multiple fallback selectors and optional AI-powered recovery.

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** Playwright browser not found
```bash
playwright install chromium
```

**Issue:** Permission denied on Linux
```bash
chmod +x venv/bin/activate
```

**Issue:** Streamlit not opening
```bash
streamlit run app.py --server.headless true
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/) - Amazing browser automation
- [Streamlit](https://streamlit.io/) - Beautiful UI framework
- [LangChain](https://langchain.com/) - LLM orchestration
- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent workflows

---

<div align="center">

### ⭐ Star this repo if you find it useful! ⭐

**Made with ❤️ in Bangalore, India**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/ai-web-testing-agent?style=social)](https://github.com/yourusername/ai-web-testing-agent)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/ai-web-testing-agent?style=social)](https://github.com/yourusername/ai-web-testing-agent)

</div># 🤖 AI Web Testing Agent

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Playwright](https://img.shields.io/badge/Playwright-Latest-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**An intelligent AI-powered agent that performs automated end-to-end (E2E) testing on web applications using natural language instructions.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Examples](#-examples) • [Architecture](#-architecture)

</div>

---

## 🎯 Overview

This project implements an intelligent agent capable of performing automated web testing using **natural language commands**. Simply describe what you want to test, and the AI agent will:

1. **Interpret** your natural language instructions
2. **Generate** executable Playwright test scripts
3. **Execute** tests in a headless browser
4. **Produce** detailed test reports with screenshots and videos

No more writing complex test scripts manually - just describe what you want to test in plain English!

---

## ✨ Features

### 🌐 Multi-Site Support
- **Amazon** - Search products, add to cart, navigate listings
- **Instagram** - Login, logout, navigate feed
- **Google Maps** - Get directions to any location
- **Google Forms** - Auto-fill and submit forms
- **Generic Websites** - Works with any website

### 🧠 Smart Automation
- **Natural Language Processing** - Understands plain English commands
- **Self-Healing Selectors** - Automatically recovers from selector failures
- **Site Detection** - Adapts behavior based on detected website
- **Smart Waits** - Intelligent DOM and network state detection

### 📊 Comprehensive Reporting
- **Screenshots** - Captures every step automatically
- **Video Recording** - Full test session recordings
- **Detailed Logs** - Step-by-step execution logs
- **HTML/JSON/PDF Reports** - Multiple export formats

### 🎨 Modern UI
- **Cyberpunk Theme** - Stunning orange industrial design
- **Real-time Logs** - Watch test execution live
- **Interactive Controls** - Easy-to-use interface

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/ai-web-testing-agent.git
cd ai-web-testing-agent
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Playwright Browsers
```bash
playwright install chromium
```

### Step 5: Set Up Environment Variables (Optional)
```bash
cp .env.example .env
# Edit .env and add your API keys if using AI selector healing
```

### Step 6: Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 📖 Usage

### Basic Syntax
```
Go to [URL] then [action1] then [action2] then ...
```

### Supported Actions

| Action | Syntax | Example |
|--------|--------|---------|
| **Navigate** | `go to [URL]` | `go to https://amazon.in` |
| **Search** | `search for '[text]'` | `search for 'iPhone 15'` |
| **Click** | `click [element]` | `click submit button` |
| **Type** | `type "[text]" in [field]` | `type "hello" in email` |
| **Login** | `login with "[user]" "[pass]"` | `login with "user@email.com" "pass123"` |
| **Logout** | `logout` | `logout` |
| **Add to Cart** | `add to cart` | `add to cart` |
| **Select Product** | `select [nth] product` | `select first product` |
| **Get Directions** | `get directions to [place]` | `get directions to Bangalore Palace` |
| **Fill Form** | `fill form` | `fill form` |
| **Wait** | `wait [n] seconds` | `wait 5 seconds` |
| **Scroll** | `scroll [direction]` | `scroll down` |
| **Screenshot** | `take screenshot` | `take screenshot` |
| **Verify** | `verify "[text]"` | `verify "Success"` |

---

## 💡 Examples

### 🛒 Amazon Shopping
```
Go to https://www.amazon.in then search for 'iPhone 15 Pro' then add to cart
```

### 📸 Instagram Login
```
Go to https://www.instagram.com then login with "your_username" "your_password"
```

### 🗺️ Google Maps Directions
```
Get directions to Lalbagh Botanical Garden Bangalore
```

### 🔍 Google Search
```
Go to https://www.google.com then search for 'AI testing automation'
```

### 📝 Form Filling
```
Go to https://docs.google.com/forms/d/your-form-id then fill form
```

### 🔗 Multi-Step Workflow
```
Go to https://www.amazon.in then search for 'laptop' then select first product then add to cart then take screenshot
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
│                    (Streamlit - Cyberpunk UI)                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Instruction Parser                           │
│              (Natural Language → Actions)                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Executor Engine                           │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│    │   Amazon     │  │  Instagram   │  │ Google Maps  │        │
│    │   Handler    │  │   Handler    │  │   Handler    │        │
│    └──────────────┘  └──────────────┘  └──────────────┘        │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│    │Google Forms  │  │   Generic    │  │  AI Healer   │        │
│    │   Handler    │  │   Handler    │  │  (Fallback)  │        │
│    └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Playwright Browser                          │
│                   (Headless Chrome/Chromium)                     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Reporter Module                             │
│         (Screenshots, Videos, HTML/JSON/PDF Reports)             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
ai_web_tester/
├── app.py                      # Streamlit UI (Cyberpunk Theme)
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
│
├── agent/
│   ├── __init__.py
│   ├── parser.py              # Natural language parser
│   ├── executor.py            # Test execution engine
│   ├── reporter.py            # Report generation
│   ├── ai_selector.py         # AI-powered selector healing
│   ├── smart_waits.py         # Intelligent wait strategies
│   ├── graph.py               # LangGraph workflow
│   ├── graph_batch.py         # Batch execution support
│   ├── code_generator.py      # Dynamic code generation
│   └── parallel_executor.py   # Parallel test execution
│
└── tests/
    ├── screenshots/           # Test screenshots
    └── videos/                # Test recordings
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.9+** | Core programming language |
| **Playwright** | Browser automation |
| **Streamlit** | Web UI framework |
| **LangGraph** | Agent workflow orchestration |
| **LangChain** | LLM integration |

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Optional: For AI-powered selector healing
GOOGLE_API_KEY=your_google_api_key
XAI_API_KEY=your_xai_api_key

# Browser settings
HEADLESS=true
TIMEOUT=30000
```

### Settings in UI

- **Headless Mode**: Run browser invisibly (faster)
- **Timeout**: Maximum wait time for elements
- **Video Recording**: Enable/disable test recordings

---

## 🎨 UI Themes

The application features a stunning **Cyberpunk Industrial** theme with:
- 🟠 Orange and amber color scheme
- ⚡ Animated backgrounds
- 🔶 Hexagonal patterns
- ⚠️ Warning stripe aesthetics
- 💀 Military/tech terminology

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/ai-web-testing-agent.git

# Install dev dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest

# Format code
black .
```

---

## 📋 Roadmap

- [x] Amazon support (search, add to cart)
- [x] Instagram login/logout
- [x] Google Maps directions
- [x] Google Forms filling
- [x] Screenshot capture
- [x] Video recording
- [x] Cyberpunk UI theme
- [x] Self-healing selectors
- [ ] Facebook support
- [ ] Twitter/X support
- [ ] LinkedIn support
- [ ] API endpoint for CI/CD integration
- [ ] Docker containerization
- [ ] Cloud deployment (AWS/GCP)
- [ ] Mobile browser testing
- [ ] Parallel test execution
- [ ] Test scheduling
- [ ] Slack/Discord notifications

---

## ❓ FAQ

### Q: Does it work with any website?
**A:** Yes! While it has optimized handlers for Amazon, Instagram, Google Maps, and Forms, it works with any website using generic selectors.

### Q: Is it free to use?
**A:** Yes, the core functionality is completely free. AI-powered selector healing requires API keys (optional).

### Q: Can I run it in CI/CD pipelines?
**A:** Yes! Run with `headless=True` for CI/CD environments. API endpoint support coming soon.

### Q: Does it support mobile testing?
**A:** Currently supports desktop browsers. Mobile emulation is on the roadmap.

### Q: What if a selector fails?
**A:** The agent has self-healing capabilities with multiple fallback selectors and optional AI-powered recovery.

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** Playwright browser not found
```bash
playwright install chromium
```

**Issue:** Permission denied on Linux
```bash
chmod +x venv/bin/activate
```

**Issue:** Streamlit not opening
```bash
streamlit run app.py --server.headless true
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/) - Amazing browser automation
- [Streamlit](https://streamlit.io/) - Beautiful UI framework
- [LangChain](https://langchain.com/) - LLM orchestration
- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent workflows

---

<div align="center">

### ⭐ Star this repo if you find it useful! ⭐

**Made with ❤️ in Bangalore, India**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/ai-web-testing-agent?style=social)](https://github.com/yourusername/ai-web-testing-agent)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/ai-web-testing-agent?style=social)](https://github.com/yourusername/ai-web-testing-agent)

</div>
