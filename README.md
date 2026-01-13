Here is the **entire corrected, clean README.md** with **all conflicts removed**.
You can **copy–paste this exactly** into your `README.md`, save it, then run `git add README.md`.

---

```markdown
# Infy-2005 – AI-Driven Test Automation System

Infy-2005 is an **AI-driven, natural language based test automation framework** that converts plain English test cases into **real browser automation** using Playwright. The system is built completely from scratch with a clean, scalable architecture suitable for **academic projects, portfolios, and future productization**.

---

## 🚀 Key Features

- Write UI test cases in **plain English**
- Agent-based orchestration using **LangGraph**
- Real browser automation using **Playwright**
- **Headless execution** for fast and silent runs
- Professional **structured test reports**
- Clean **Streamlit UI** for execution and visualization
- macOS-safe backend configuration

---

## 🧠 System Overview

The system follows a layered architecture:

```

User (Streamlit UI)
↓
Flask API (/run-test)
↓
LangGraph Workflow
↓
Instruction Parser
↓
Playwright Executor (Headless)
↓
Report Formatter
↓
UI Dashboard

```

Each component is decoupled, making the system extensible and easy to maintain.

---

## 🛠 Technology Stack

| Layer              | Technology            |
|--------------------|-----------------------|
| Language           | Python 3.11           |
| Frontend           | Streamlit             |
| Backend            | Flask                 |
| Workflow Engine    | LangGraph             |
| Browser Automation | Playwright            |
| Reporting          | Custom JSON Formatter |
| OS                 | macOS                 |

---

## 📁 Project Structure

```

infy-2005/
│
├── backend/
│   ├── app.py                  # Flask entry point
│   ├── agents/
│   │   ├── graph.py             # LangGraph workflow
│   │   ├── parser.py            # Instruction parser
│   │   └── executor.py          # Playwright executor
│   ├── reports/
│   │   └── formatter.py         # Report generator
│   └── utils/
│
├── frontend/
│   └── streamlit_app.py         # Streamlit UI
│
├── tests/
│   └── static/
│       └── demo.html            # Demo test page
│
├── .gitignore
└── README.md

````

---

## ⚙️ Setup Instructions (macOS)

### 1️⃣ Clone / Create Project

```bash
mkdir infy-2005
cd infy-2005
````

### 2️⃣ Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install flask streamlit playwright langgraph
playwright install
```

---

## ▶️ Running the Application

### Start Backend (Flask)

```bash
python backend/app.py
```

Backend runs on:

```
http://127.0.0.1:5001
```

### Start Frontend (Streamlit)

```bash
streamlit run frontend/streamlit_app.py
```

UI available at:

```
http://localhost:8501
```

---

## ✍️ Writing a Test Case

Example natural language test case:

```
Open the page
Enter email
Click submit
Verify success
```

The system automatically:

* Parses instructions
* Executes browser actions
* Validates UI behavior
* Generates a test report

---

## 📊 Sample Report Output

```json
{
  "metadata": {
    "executed_at": "2026-01-07T10:30:00Z",
    "engine": "Infy-2005 AI Test Engine",
    "mode": "headless"
  },
  "summary": {
    "total": 4,
    "passed": 4,
    "failed": 0
  },
  "steps": [
    {"step": "Open page", "status": "PASS"},
    {"step": "Fill email", "status": "PASS"},
    {"step": "Click submit", "status": "PASS"},
    {"step": "Verify success", "status": "PASS"}
  ]
}
```

---

## 🧩 Key Modules Explained

### 🔹 Parser

Converts natural language instructions into structured steps.

### 🔹 LangGraph Workflow

Controls execution order and state passing between agents.

### 🔹 Executor

Uses Playwright to perform browser actions in headless mode.

### 🔹 Reporter

Formats execution results into structured, professional reports.

---

## 🧪 Demo Test Page

A local HTML page (`demo.html`) is used to:

* Ensure deterministic automation
* Avoid external dependencies
* Validate DOM interactions

---

## 🚧 Challenges Solved

* Python version incompatibility
* LangChain import changes
* Circular imports
* macOS port conflicts
* Playwright setup issues

Each challenge was resolved to improve system robustness.

---

## 🌱 Future Enhancements

* LLM-based instruction parsing (OpenAI / local LLM)
* Batch test execution
* HTML / PDF report export
* CI/CD integration
* Visual DOM selector intelligence

---

## 🎯 Use Cases

* Academic final-year project
* QA automation portfolio
* AI + testing research
* Startup prototype

---

## 📌 Conclusion

Infy-2005 demonstrates how **AI, automation, and clean architecture** can be combined to build a modern testing platform. The system is stable, extensible, and suitable for real-world applications.

---

**Author:** Bharanitharann Nagendram
**Project:** Infy-2005 AI Test Automation

````


