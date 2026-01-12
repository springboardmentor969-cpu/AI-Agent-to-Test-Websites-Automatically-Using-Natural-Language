# AI Agents to Test Websites Automatically Using Natural Language

## Project Overview

This project implements an AI-based system to automatically test websites using **natural language instructions**.
Instead of manually writing test scripts, users can describe test steps in plain English, and the system converts them into **Playwright automation scripts**, executes them in a **headless browser**, validates results using assertions, and returns a **PASS/FAIL** status.

## Problem Statement

Manual website testing is time-consuming and requires technical expertise.
This project simplifies web testing by allowing users to provide test instructions in natural language and automatically executing them using AI agents.

## Technologies Used

* Python
* Flask
* LangGraph
* LangChain
* Playwright
* HTML, CSS, JavaScript
* 
## Project Structure
project/
│
├── app.py
├── requirements.txt
│
├── agent/
│   ├── __init__.py
│   ├── lang_agent.py
│   ├── parser.py
│   ├── playwright_generator.py
│   ├── assertion_generator.py
│   └── executor.py
│
├── templates/
│   ├── index.html
│   └── sample_form.html

## Milestones Implementation

### Milestone 1 & 2

* Python environment setup
* Flask server initialization
* Basic LangGraph agent configuration
* Natural language instruction parsing
* Static HTML test page

### Milestone 3 (Week 5–6)

* Automatic Playwright code generation
* Assertion generation for validation
* Headless browser execution
* Execution logs and PASS/FAIL result
* Testing on local HTML forms

## System Workflow

1. User enters a test instruction in natural language.
2. The instruction is parsed into structured test steps.
3. Playwright automation commands are generated.
4. Tests are executed in a headless Chromium browser.
5. Assertions validate the execution.
6. Results are returned as structured JSON.

## Sample Input
open local page and click submit
## Sample Output
json
{
  "parsed_steps": [
    {
      "action": "open_browser",
      "url": "http://127.0.0.1:5000/sample_form.html"
    },
    {
      "action": "click",
      "selector": "#submit"
    }
  ],
  "execution_log": [
    "page.goto(\"http://127.0.0.1:5000/sample_form.html\")",
    "page.click(\"#submit\")",
    "assert page.title() != ''"
  ],
  "result": "PASS"
}

## Installation Steps

### Step 1: Create Virtual Environment
python -m venv venv
### Step 2: Activate Virtual Environment
Windows:
venv\Scripts\activate
source venv/bin/activate
### Step 3: Install Dependencies
pip install -r requirements.txt
### Step 4: Install Playwright Browsers
playwright install
## How to Run the Project
python app.py
Open browser and go to:
http://127.0.0.1:5000
## Execution Mode
* Tests run in **headless mode**
* Browser UI is not visible
* Real page loading and actions occur in the background
* Suitable for automation and CI/CD pipelines
## Key Advantages
* No manual test scripting required
* Natural language based testing
* Real browser execution
* Scalable and automation-friendly
* Beginner-friendly interface
## Conclusion
This project demonstrates how AI agents can automate website testing using natural language.
It reduces manual effort, improves efficiency, and provides a strong foundation for intelligent testing systems.


Cheppu 👍
