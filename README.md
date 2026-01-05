# AI Agent to Test Websites Automatically Using Natural Language

An AI-powered web testing tool that allows users to test websites using natural language instructions. Built with **Flask**, **LangGraph**, and **Playwright**, the system provides a scalable foundation for automated browser testing using AI-driven workflows.

## 🎯 Project Overview

This project implements an intelligent agent capable of performing automated end-to-end (E2E) testing on web applications. The agent:
- Accepts natural language test instructions
- Parses and interprets test steps
- Generates executable Playwright scripts
- Provides structured test assertions

## 🏗️ Architecture

```
User Input (Natural Language)
        ↓
┌─────────────────────────────────────┐
│         LangGraph Workflow          │
│                                     │
│   ┌─────────────┐    ┌───────────┐  │
│   │ Instruction │ →  │   Code    │  │
│   │   Parser    │    │ Generator │  │
│   └─────────────┘    └───────────┘  │
└─────────────────────────────────────┘
        ↓
Playwright Test Scripts + Assertions
```

## 📁 Project Structure

```
AATW/
├── app.py                  # Flask application entry point
├── requirements.txt        # Python dependencies
├── agent/
│   ├── __init__.py
│   ├── instruction_parser.py   # NL → Structured commands
│   ├── code_generator.py       # Commands → Playwright scripts
│   └── langgraph_agent.py      # LangGraph workflow orchestration
├── templates/
│   └── index.html          # Web interface
└── static/
    └── styles.css          # UI styling
```

## 🧩 Modules

### 1. Instruction Parser Module (`agent/instruction_parser.py`)
Interprets natural language test descriptions and maps them to browser actions:
- Page navigation (open, navigate, go to)
- Text input (enter, type, fill)
- Click actions (click, submit, press)
- Verification (verify, check, assert)
- Wait actions

### 2. Code Generator Module (`agent/code_generator.py`)
Converts parsed actions into executable Playwright Python scripts:
- Generates complete test functions
- Maps actions to Playwright API calls
- Creates dynamic assertions

### 3. LangGraph Agent (`agent/langgraph_agent.py`)
Orchestrates the workflow using LangGraph StateGraph:
- Defines typed state schema
- Connects parser → code generator nodes
- Compiles and executes the workflow

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AATW
   ```

2. **Create virtual environment**
   ```bash
   python -m venv projenv
   projenv\Scripts\activate  # Windows
   # source projenv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers** (for test execution)
   ```bash
   playwright install
   ```

## 💻 Usage

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open the web interface**
   Navigate to `http://localhost:5000`

3. **Enter natural language test instructions**
   Examples:
   - `"Open the home page and click the login button"`
   - `"Navigate to dashboard and verify success message"`
   - `"Enter 'testuser' in username and 'pass123' in password, then submit"`

4. **View the response**
   - Parsed actions (structured commands)
   - Generated Playwright code
   - Assertions for validation

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/test` | POST | Process test instruction |
| `/health` | GET | Health check |

### Example API Request
```bash
curl -X POST http://localhost:5000/test \
  -H "Content-Type: application/json" \
  -d '{"instruction": "Open home page and click login button"}'
```

## 🛠️ Technology Stack

- **Flask** - Web framework and REST API
- **LangGraph** - Agent workflow orchestration
- **Playwright** - Browser automation
- **Python 3.x** - Programming language

## 📋 Milestones Completed

### Milestone 1 (Week 1-2) ✅
- [x] Python environment setup
- [x] Dependencies installation (LangGraph, Playwright, Flask)
- [x] Project structure defined
- [x] Flask server with static HTML test page
- [x] LangGraph agent configuration

### Milestone 2 (Week 3-4) ✅
- [x] Instruction Parser Module
- [x] Structured command mapping
- [x] LangGraph workflow (parser → code generator)
- [x] Code Generator Module
- [x] Test case conversion validation

## 📄 License

MIT License - see LICENSE file for details.
