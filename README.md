# AI-Based Website Testing Automation System

## 📌 Project Overview

This project implements an **AI-based automated website testing system** that converts **natural language test instructions** into **automated browser actions** using **Playwright**.  
The system executes tests in a **headless browser**, validates results using **assertions**, generates **execution reports**, and captures **screenshots automatically on failure**.

The project is developed milestone-wise, following a modular and scalable architecture.

## 🎯 Objectives

- Accept test instructions in plain English
- Automatically generate browser automation scripts
- Execute tests using Playwright
- Validate results using assertions
- Generate structured test reports
- Capture screenshots for failed test cases

## 🛠️ Technologies Used

- **Python**
- **Flask** – Backend server
- **Playwright** – Browser automation
- **LangGraph** – Agent workflow orchestration
- **HTML & CSS** – User interface
- **JSON** – Test reporting format

## 📁 Project Folder Structure

project/
│
├── app.py
├── requirements.txt
│
├── agent/
│ ├── init.py
│ ├── parser.py
│ ├── playwright_generator.py
│ ├── assertion_generator.py
│ ├── executor.py
│ └── lang_agent.py
│
├── templates/
│ ├── index.html
│ └── sample_form.html
│
├── reports/
│ └── reports.json
│
├── screenshots/
│ └── fail_YYYYMMDD_HHMMSS.png

## Milestone Summary

### Milestone 1 – Instruction Parsing
- User enters test instruction in English.
- Instruction is parsed into structured test steps.

### Milestone 2 – Agent Workflow
- LangGraph agent manages the test flow.
- Parsing, execution, and result handling are connected.

### Milestone 3 – Test Execution
- Playwright code is generated dynamically.
- Tests run in a headless Chromium browser.
- Assertions decide PASS or FAIL.

### Milestone 4 – Reporting & Screenshots
- Test results are saved in `reports.json`.
- Screenshots are captured **only when a test fails**.
- PASS → Report only  
- FAIL → Report + Screenshot

## How to Run

```bash
pip install -r requirements.txt
playwright install
python app.py

