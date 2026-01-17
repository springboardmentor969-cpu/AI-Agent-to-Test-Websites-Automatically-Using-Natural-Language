# AI-Based Automated Test Case Generation System

## Overview
This project presents an AI-based system designed to automate end-to-end web application
testing using natural language instructions. The system allows users to describe test
scenarios in plain English, which are automatically converted into executable browser
automation scripts.

By reducing the need for manual scripting, the project simplifies test automation and
makes it accessible to both technical and non-technical users.

---

## Problem Statement
Manual creation of automated test cases is time-consuming, repetitive, and requires
strong technical expertise. Traditional automation frameworks rely heavily on scripting,
which increases development effort and limits usability.

There is a need for an intelligent system that can understand natural language test
instructions and automatically generate, execute, and validate test cases.

---

## Solution Approach
The proposed solution uses Natural Language Processing (NLP) to interpret user-provided
test instructions and convert them into automated Playwright test scripts. The system
follows a modular architecture that separates responsibilities such as instruction
parsing, test generation, execution, and reporting.

This approach improves scalability, maintainability, and clarity of the testing workflow.

---

## System Architecture
The system consists of the following major components:
- User Interface for accepting natural language instructions
- NLP Parser to interpret test steps
- Test Case Generator to create Playwright scripts
- Test Executor to run automated tests in a headless browser
- Report Generator to produce structured test results

A high-level architecture diagram is provided as part of Milestone-01 documentation.

---

## Project Structure
infosys-ai-test-automation/
│
├── src/ # Application source code
│ ├── app.py
│ ├── workflow.py
│ ├── ui.py
│ ├── agent/
│ ├── executor/
│ └── report/
│
├── samples/ # Sample HTML pages
│ └── form.html
│
├── milestones/ # Milestone-wise documentation
│ ├── milestone-01-problem-design/
│ ├── milestone-02-implementation/
│ ├── milestone-03-testing-validation/
│ └── milestone-04-final-submission/
│
├── requirements.txt
└── README.md


---

## Milestones

### Milestone 01 – Problem Definition & Design
- Analysis of the testing problem
- Identification of challenges in manual automation
- Design of a modular system architecture
- Architecture diagram and design documentation

### Milestone 02 – Implementation
- Module-wise implementation of the system
- Natural language instruction parsing
- Automated test script generation
- Implementation workflow / code flow diagram

### Milestone 03 – Testing & Validation
- Execution of generated test cases
- Validation of expected vs actual outcomes
- Confirmation of system reliability and correctness

### Milestone 04 – Final Submission
- Consolidated project documentation
- Results summary
- Limitations and future enhancement scope

---

## Technologies Used
- Programming Language: Python
- Backend Framework: Flask
- Automation Tool: Playwright
- Natural Language Processing: Rule-based NLP
- Documentation: Markdown

---

## How to Run the Project
1. Install dependencies:



---

## Results
The system successfully converts natural language instructions into automated test cases
and executes them reliably. This significantly reduces manual effort and improves testing
efficiency.

---

## Future Enhancements
- Integration of advanced NLP and AI models
- Support for mobile and API testing
- CI/CD pipeline integration
- Enhanced reporting and analytics dashboard

---

## Conclusion
This project demonstrates the effective use of AI and natural language processing to
simplify automated testing. The clean architecture, milestone-based development, and
modular implementation make the system scalable and suitable for real-world testing
scenarios.
