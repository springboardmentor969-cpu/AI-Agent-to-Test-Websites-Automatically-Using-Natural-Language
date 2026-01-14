# AI Agent to Test Websites Automatically Using Natural Language

## Project Overview
This project implements an AI-based automated website testing system where users can write test instructions in natural language.  
The system converts these instructions into browser automation steps, executes them using Playwright, validates results using assertions, and generates execution reports with screenshots on failure.

## Key Features
- Natural language based test instructions
- Automated browser testing using Playwright
- Headless browser execution
- PASS / FAIL result validation
- JSON-based test reports
- Automatic screenshot capture on failure

## Technologies Used
- Python
- Flask
- Playwright
- LangGraph
- HTML, CSS

## Project Folder Structure
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

