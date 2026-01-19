# AI Website Testing Agent

**Automated Website Testing using Natural Language and Playwright**

---

## 1. Project Overview

This project implements an intelligent agent capable of performing automated end-to-end (E2E) testing of web applications using **natural language instructions**.
Instead of writing manual test scripts, the user provides instructions in simple English, which are automatically converted into Playwright automation steps, executed in a browser, and reported as pass or fail results.

---

## 2. Objective

The main objective of this project is to:

* Reduce manual effort in writing test cases
* Demonstrate how natural language can be used for automated testing
* Implement an end-to-end testing workflow suitable for academic demonstration

---

## 3. System Workflow

The project follows a step-by-step testing pipeline:

1. **Instruction Input**
   The user enters a test instruction through the UI.

2. **Instruction Parsing**
   The system interprets the natural language instruction and identifies the required action.

3. **Code Generation**
   The instruction is converted into Playwright automation steps.

4. **Execution**
   The generated steps are executed automatically in a headless browser.

5. **Assertion & Validation**
   Assertions are applied to verify whether the test executed successfully.

6. **Reporting**
   A structured test report is generated showing pass or fail results.

---

## 4. Project Structure

```
infosys-project/
│
├── agent/                  # Instruction parsing, code generation, assertions
├── executor/               # Test execution logic
├── report/                 # Test reporting module
├── samples/                # Sample HTML pages for testing
├── src/                     # Main application files
│   ├── app.py               # Backend controller (Flask)
│   ├── ui.py                # User Interface (Streamlit)
│   └── workflow.py          # Workflow logic
├── requirements.txt         # Project dependencies
├── Readme.md                # Project documentation
```

---

## 5. Milestone Implementation

### Milestone 1 (Week 1–2)

* Python environment setup
* Dependency installation
* Project structure creation
* Basic Flask backend initialization

### Milestone 2 (Week 3–4)

* Natural language instruction parser
* Mapping instructions to structured actions
* Workflow setup between modules

### Milestone 3 (Week 5–6)

* Playwright automation code generation
* Assertion engine for validation
* Headless browser execution logic
* Functional test execution

### Milestone 4 (Week 7–8)

* Test reporting module
* Error handling and result validation
* Streamlit-based user interface
* End-to-end system integration

---

## 6. Technology Stack

* **Programming Language:** Python 3.x
* **Frameworks / Tools:**

  * Flask (Backend API)
  * Playwright (Browser Automation)
  * Streamlit (User Interface)
  * LangGraph (Workflow orchestration – conceptual)

---

## 7. How to Run the Project

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run Backend (Milestone 3 Engine)

From project root:

```bash
python src/app.py
```

Backend runs at:

```
http://127.0.0.1:5000
```

(Note: This page is intentionally blank.)

---

### Step 3: Run UI (Milestone 4 Integration)

Open a new terminal:

```bash
python -m streamlit run src/ui.py
```

UI runs at:

```
http://localhost:8501
```

---

## 8. Sample Test Instructions

```
open google
search automation
```

---

## 9. Output

The system displays:

* Total test steps
* Passed steps
* Failed steps
* Step-by-step execution status

---

## 10. Conclusion

This project demonstrates a complete automated testing workflow using natural language input and browser automation.
It successfully integrates instruction parsing, test execution, and reporting into a single end-to-end system suitable for academic evaluation.

---

## 11. Author
## Author

**Ayan Hamdan** is the developer of the project *AI Website Testing Agent*.
This project was developed as an academic submission to demonstrate the use of natural language processing and browser automation for automated website testing.

The work focuses on converting user-defined natural language instructions into automated Playwright test executions, validating results, and presenting structured pass/fail reports through an integrated system. The project reflects practical understanding of software testing concepts, backend integration, and end-to-end system design.

