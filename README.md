# AI Web Testing Agent 🤖🌃🦾

Minimalist, powerful, and ultra-futuristic autonomous web testing engine. Built for reliability, precision, and high-impact visual reporting.

![Version](https://img.shields.io/badge/version-1.0-blueviolet?style=for-the-badge)
![UI](https://img.shields.io/badge/UI-Vibrant_Futurism-darkblue?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Grok_(xAI)_Healer-neon?style=for-the-badge)

## 🌌 Key Features
- **"Unbreakable" AI Execution**: Combines local heuristics with **Grok (xAI)** intelligence to heal broken selectors in real-time.
- **Cyber-Noir Dashboard**: A cinematic, high-fidelity UI with animated backgrounds and tactical display modules.
- **Direct Reporting**: Instant visibility of HTML audit reports with tiled screenshots and integrated video playback.
- **Professional Exports**: Generate and download one-click **PDF and HTML** audit reports with embedded evidence.
- **Windows Optimized**: Built-in support for Windows asyncio policies to ensure zero execution errors.

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
source projenv310/bin/activate  # Windows: projenv310\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 3. Configuration
Rename `.env.example` to `.env` and add your credentials:
```env
GROK_API_KEY=your_key_here
```

### 4. Running the App
```bash
streamlit run ui/app.py
```

## 🛠️ Tech Stack
- **Engine**: LangGraph, Playwright
- **AI**: Grok (xAI) via LangChain
- **Interface**: Streamlit (with Custom Cyberpunk CSS)
- **Reporting**: FPDF2, Jinja2

## 🛡️ Architecture
The agent uses a **State-Based Batch Execution** model:
1. **Instruction Parsing**: Converts plain English steps into actionable JSON sequences.
2. **Parallel Execution**: Runs tests simultaneously across independent browser contexts.
3. **AI Healing**: If a selector fails, the **AI Healer** analyzes the DOM and generates a new stable path instantly.
4. **Autonomous Reporting**: Aggregates logs, captures, and builds professional audit exports.

---
Built with ❤️ for the future of automated testing. 🚀🤖🏁
