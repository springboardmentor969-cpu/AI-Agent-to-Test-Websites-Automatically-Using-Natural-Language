# 🤖 AI Agent for Automated Web Testing using Natural Language

## 📌 Project Overview

This project presents an AI-powered web automation agent that converts natural language test instructions into executable browser automation workflows.

Instead of writing manual Selenium or Playwright scripts, users can simply describe their test scenarios in plain English. The system intelligently interprets the instruction using a Large Language Model (Groq LLaMA 3.3), generates structured automation steps in JSON format, executes them using Playwright, and produces a structured execution report.

This significantly reduces manual scripting effort and makes test automation accessible to non-technical users.

---

## 🎯 Problem Statement

Traditional automation frameworks require:

* Programming knowledge
* Manual selector writing
* Script maintenance
* Frequent updates due to UI changes

Non-technical users cannot easily create automation tests.

This project solves that by enabling:

> Automated website testing using natural language commands.

---

## 🧠 System Architecture

### Step-by-Step Flow

1️⃣ User enters test instruction in plain English
2️⃣ Groq LLM converts instruction into structured JSON steps
3️⃣ Parser validates and processes steps
4️⃣ Playwright dynamically executes steps in headless browser
5️⃣ Assertions are applied
6️⃣ Reporter generates pass/fail test result

---

## 🏗️ Updated Project Structure

```
ai_agent_web_testing/
│
├── app.py                  # Flask entry point
│
├── agent/
│   ├── __init__.py
│   ├── groq_agent.py           # LLM instruction converter
│   ├── parser.py               # JSON step validation
│   ├── executor.py             # Execution controller
│   ├── playwright_generator.py # Playwright script generator
│   ├── playwright_runner.py    # Browser execution engine
│   ├── assertion_generator.py  # Assertion logic
│   ├── reporter.py             # Test reporting module
│   ├── langgraph_agent.py      # Workflow orchestration
│
├── templates/
│   └── index.html              # Frontend UI
│
├── reports/                    # Generated reports
│
├── .env                        # GROQ_API_KEY
├── requirements.txt
└── README.md
```

---

## 🛠️ Technologies Used

* Python
* Flask
* Groq API (LLaMA 3.3 70B Model)
* LangGraph
* Playwright
* JSON
* HTML / CSS / JavaScript

---

## 🚀 Key Features

✔ Natural Language Test Execution
✔ LLM-based Step Generation
✔ Dynamic JSON Automation Flow
✔ Headless Browser Execution
✔ Assertion Validation
✔ Structured Test Reporting
✔ Modular Agent Architecture
✔ Error Handling & Adaptability

---

## 🧠 Why Groq API?

* Ultra-fast inference
* Cost-efficient
* Strong instruction-following capability
* Handles structured JSON generation effectively

---

## 📊 Output

The system generates:

* Structured JSON test steps
* Real-time browser execution
* Pass/Fail test status
* Execution logs
* Error trace (if failure occurs)

---

## ▶️ How to Run the Project

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Install Playwright Browsers

```bash
playwright install
```

### 3️⃣ Add Environment Variable

Create `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

### 4️⃣ Run Application

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## 📈 Innovation & Uniqueness

* Combines LLM + Automation Testing
* Converts English instructions to executable automation
* Reduces dependency on technical scripting
* Supports scalable agent-based architecture
* Can be extended for CI/CD integration

---

## 👩‍💻 Developed By

**Kaya Dhankar**
- B.Tech CSE (Artificial Intelligence)
