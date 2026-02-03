# 🤖 AI Agent to Test Websites Automatically Using Natural Language

## 📌 Project Overview
This project implements an AI-powered web testing agent that converts natural language test instructions into executable browser automation scripts. It eliminates the need for manual scripting by allowing users to describe test cases in plain English.

The system uses a LangGraph-based agent to parse instructions, generate Playwright automation code, execute tests in a headless browser, and produce structured test reports.

---

## 🎯 Problem Statement
Traditional web automation tools require coding knowledge, making them inaccessible to non-technical users. This project solves that problem by enabling automated testing through natural language inputs.

---

## 🧠 Solution Architecture
1. User enters test instructions in plain English
2. Instruction Parser converts text into structured actions
3. LangGraph workflow manages execution flow
4. Playwright code is generated dynamically
5. Headless browser executes the test
6. Reporting module generates execution results

---

---
🚀 Features

🌐 Web UI to run tests easily

🧠 AI Agent that understands natural language test instructions

🧪 Automated testing using Playwright

📄 Assertion generation using AI

📊 Test reports generation

⚙️ Modular and scalable architecture

---

## 🏗️ Project Structure
ai_agent_web_testing/
│
├── app.py
├── agent/
│ ├── __init__.py
│ ├── assertion_generator.py
│ ├── parser.py
│ ├── executor.py
│ ├── reporter.py
│ ├── langgraph_agent.py
│ ├── playwright_generator.py
│ ├── playwright_runner.py
│
├── templates/
│ └── index.html
│
├── static/
│ └── login.html
│
├── README.md
└── requirements.txt

---

## 🛠️ Technologies Used
- Python
- Flask
- Playwright
- HTML / CSS / JavaScript
- JSON
- AI / NLP: LLM-based agent (LangGraph style)

---

## 🚀 Milestones Completed

### ✅ Milestone 1
- Environment setup and dependency installation
- Flask server initialization
- Baseline LangGraph agent configuration

### ✅ Milestone 2
- Natural language instruction parser
- Structured command mapping
- LangGraph workflow integration

### ✅ Milestone 3
- Playwright code generation
- Assertion creation
- Headless browser execution

### ✅ Milestone 4
- Reporting module implementation
- Error handling and DOM adaptability
- UI finalization
- End-to-end execution workflow
- Documentation and demo preparation

---

## 📊 Output
- Parsed test steps in structured JSON
- Automated browser execution
- Pass/Fail test report with execution details

---

## ▶️ How to Run the Project
```bash
pip install -r requirements.txt
playwright install
python app.py
```

## 👩‍💻 Developed By
- Kaya Dhankar
- B.Tech CSE (AI)
