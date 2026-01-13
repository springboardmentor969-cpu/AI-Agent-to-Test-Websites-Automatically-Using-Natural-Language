# Infy-2005 – AI-Driven Test Automation System

Infy-2005 is an AI-driven, natural language–based test automation system that converts plain English test instructions into real browser automation using Playwright.

The project is built from scratch with a clean, scalable architecture and is suitable for academic final-year projects, professional portfolios, research experimentation, and future productization.

---

## Project Vision

Traditional UI automation frameworks require writing complex scripts.  
Infy-2005 simplifies this by allowing users to describe test cases in natural language and automatically execute them in a real browser.

The long-term goal is to evolve this into an AI-assisted testing platform with intelligent parsing, validation, and reporting.

---

## Key Features

- Natural language test case definition  
- Agent-based orchestration using LangGraph  
- Real browser automation with Playwright  
- Headless execution for speed and stability  
- Structured JSON-based test reports  
- Interactive Streamlit user interface  
- Clean separation of frontend, backend, and execution layers  
- macOS-safe development setup  

---

## System Architecture

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
Execution Results


Each layer is decoupled, making the system easy to extend and maintain.

---

## Technology Stack

| Component | Technology |
|---------|------------|
| Language | Python 3.11 |
| Frontend | Streamlit |
| Backend | Flask |
| Workflow Engine | LangGraph |
| Browser Automation | Playwright |
| Reporting | Custom JSON |
| OS | macOS |

---

## Project Structure
infy-2005/
│
├── backend/
│ ├── app.py
│ ├── agents/
│ │ ├── graph.py
│ │ ├── parser.py
│ │ ├── executor.py
│ │ └── parser_prompt.py
│ ├── reports/
│ │ ├── formatter.py
│ │ └── reporter.py
│ └── utils/
│ ├── dom_mapper.py
│ └── error_handler.py
│
├── frontend/
│ └── streamlit_app.py
│
├── tests/
│ └── static/
│ └── demo.html
│
├── static/
│ └── style.css
│
├── templates/
│ └── index.html
│
├── requirements.txt
├── .gitignore
└── README.md


---

## Setup Instructions (macOS)

### Create Virtual Environment

python3.11 -m venv venv
source venv/bin/activate


### Install Dependencies
pip install flask streamlit playwright langgraph
playwright install


---

## Running the Application

### Start Backend

python backend/app.py

Backend runs at:
http://127.0.0.1:5001


### Start Frontend

streamlit run frontend/streamlit_app.py


UI runs at:

http://localhost:8501


---

## Writing Test Cases

Example natural language test:

Open the page
Enter email
Click submit
Verify success


The system automatically:
- Parses instructions
- Executes browser actions
- Validates UI behavior
- Generates a structured report

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
    { "step": "Open page", "status": "PASS" },
    { "step": "Fill email", "status": "PASS" },
    { "step": "Click submit", "status": "PASS" },
    { "step": "Verify success", "status": "PASS" }
  ]
}

🧩 Core Modules

Instruction Parser – Converts natural language instructions into structured execution steps

LangGraph Workflow – Manages execution flow and agent state transitions

Playwright Executor – Runs real browser actions in headless mode

Reporting Engine – Generates structured and professional test reports

🧪 Demo Test Page

A local HTML page is used to:

Ensure deterministic testing

Avoid external dependencies

Validate DOM interactions reliably

🚧 Challenges Solved

Python version incompatibilities

LangChain to LangGraph migration

Circular imports

macOS port conflicts

Playwright setup issues

📌 Conclusion

Infy-2005 demonstrates how AI orchestration, browser automation, and clean architecture can be combined to build a modern testing platform.

The system is stable, extensible, and suitable for real-world learning and experimentation.

👤 Author

Bharanitharan Nagendran
Creator & Developer
Project: Infy-2005 – AI-Driven Test Automation System
