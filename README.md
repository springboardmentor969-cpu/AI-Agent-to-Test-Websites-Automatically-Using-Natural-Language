# 🤖 AI Website Testing Agent

**Automated Website Testing using Natural Language, Playwright & LangGraph**

**v2.0 - Enhanced NLP Release** ⭐

---

## 📋 Project Overview

This project implements an intelligent agent capable of performing automated end-to-end (E2E) testing of web applications using **natural language instructions**. Instead of writing manual test scripts, users provide instructions in conversational English, which are automatically converted into Playwright automation steps, executed in a browser, and reported with detailed results.

**Key Innovation:** Advanced NLP parser with regex URL detection, flexible keyword recognition, and intelligent credential extraction.

---

## 🎯 Objectives

* Reduce manual effort in writing test cases
* Demonstrate advanced NLP for automated testing
* Implement a complete end-to-end testing workflow
* Support multiple testing scenarios (navigation, search, login, form filling)
* Provide beautiful, intuitive user interface

---

## 🔄 System Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. Natural Language Input                                   │
│     Example: "open google and search automation testing"     │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│  2. Advanced NLP Parsing (NEW)                               │
│     - Detect 30+ keyword variations                         │
│     - Auto-detect URLs with regex                           │
│     - Extract credentials automatically                      │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│  3. Code Generation                                          │
│     Convert intent to Playwright steps                       │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│  4. Test Execution                                           │
│     Execute in headless browser with Playwright             │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│  5. Assertion & Validation                                   │
│     Verify page loads, elements exist, text found           │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│  6. Beautiful Reporting (NEW)                                │
│     Metrics, detailed results, clickable links              │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. System Workflow

The project follows a step-by-step testing pipeline:

1. **Instruction Input**
   The user enters a test instruction through the UI.

2. **Instruction Parsing (ENHANCED)**
   Advanced NLP with 30+ keyword variations, URL regex detection, and credential extraction.

3. **Code Generation**
   The instruction is converted into Playwright automation steps.

4. **Execution**
   The generated steps are executed automatically in a headless browser.

5. **Assertion & Validation**
   Assertions are applied to verify whether the test executed successfully.

6. **Reporting (ENHANCED)**
   Beautiful structured reports with metrics, clickable links, and detailed results

---

## 4. Project Structure

```
infosys-project/
│
├── agent/
│   ├── __init__.py
│   ├── instruction_parser.py      # ⭐ Advanced NLP parsing
│   ├── code_generator.py          # ⭐ Support for all actions
│   └── assertion_engine.py        # Validation logic
│
├── executor/
│   ├── runner.py                  # ⭐ Enhanced execution
│
├── reporting/
│   ├── report_manager.py          # ⭐ Enhanced reports
│
├── src/
│   ├── ui.py                      # ⭐ Premium Streamlit interface
│   ├── workflow.py                # LangGraph workflow
│   ├── app.py                     # Backend controller
│   └── templates/
│       └── index.html
│
├── requirements.txt
├── README.md
└── app.py
---

## 5. Milestone Implementation

### ✅ Milestone 1 (Week 1–2) - Setup
* Python environment setup
* Dependency installation
* Project structure creation

### ✅ Milestone 2 (Week 3–4) - NLP Parsing
* Natural language instruction parser
* Mapping instructions to structured actions
* Workflow setup between modules

### ✅ Milestone 3 (Week 5–6) - Code Generation & Execution
* Playwright automation code generation
* Assertion engine for validation
* Headless browser execution logic

### ✅ Milestone 4 (Week 7–8) - UI & Integration
* Test reporting module
* Streamlit-based user interface
* End-to-end system integration

### 🆕 Milestone 5 - Enhanced NLP (LATEST)
* ⭐ Advanced URL detection with regex
* ⭐ 30+ keyword variations support
* ⭐ Automatic credential extraction
* ⭐ Premium Streamlit UI with metrics
* ⭐ Clickable links in reports
* ⭐ Multi-action support (click, fill, wait)
* ⭐ Success rate metrics

---

## 6. Technology Stack

* **Programming Language:** Python 3.x

* **Frameworks / Tools:**
  * Flask (Backend API)
  * Playwright (Browser Automation)
  * Streamlit (User Interface) ⭐ NEW
  * LangGraph (Workflow orchestration)
  * Regex & URL Parsing (Advanced NLP) ⭐ NEW

---

## 7. 🚀 NEW FEATURES - Enhanced NLP (v2.0)

### ✨ Advanced Natural Language Processing

#### 🔤 Multi-keyword Recognition (30+ variations)
| Keyword Category | Variations | Example |
|-----------------|-----------|---------|
| **Navigation** | open, go to, visit, navigate | "open github.com" |
| **Search** | search, find, look for, query | "search automation testing" |
| **Auth** | login, sign in, authenticate | "login username admin password pass123" |
| **Interaction** | click, tap, press button | "click submit" |
| **Forms** | fill, type, enter, input | "fill input with data" |
| **Control** | wait, scroll, load, pause | "wait 3 seconds" |

#### 🔗 Smart URL Detection (Regex + Domain Recognition)
- ✅ Auto-detects HTTP/HTTPS URLs using regex patterns
- ✅ Normalizes URLs (adds https:// if missing)
- ✅ Recognizes popular domains: Google, GitHub, YouTube, Facebook, Twitter, LinkedIn
- ✅ Handles any custom domain

**Examples:**
```
"open google"                      → https://www.google.com
"visit github.com"                 → https://github.com  
"go to https://example.com"        → https://example.com
"navigate to facebook"             → https://www.facebook.com
```

#### 🔐 Smart Credential Extraction
- ✅ Automatically extracts username and password from text
- ✅ Flexible format support with variations

**Examples:**
```
"login username admin password pass123"
→ username: "admin", password: "pass123"

"sign in user john pass secret"
→ username: "john", password: "secret"
```

#### ⚡ Supported Test Actions
| Action | Type | Description |
|--------|------|-------------|
| **navigate** | goto | Navigate to URL |
| **search** | fill + press | Fill search and press Enter |
| **login** | fill + click | Fill credentials and login |
| **click** | click | Click buttons/elements |
| **fill** | fill | Fill form inputs |
| **wait** | wait | Pause execution |

### 🎨 Premium User Interface (NEW)

Features:
- ✅ Responsive Streamlit design
- ✅ Sidebar with comprehensive examples
- ✅ Quick action buttons (one-click demos)
- ✅ Live metrics dashboard (total, passed, failed, success rate)
- ✅ Expandable test results
- ✅ Clickable links to open detected URLs
- ✅ Tabbed interface (results vs JSON)
- ✅ Beautiful styling and emojis

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

### Navigation Examples
```
open google
visit github.com
go to https://example.com
navigate to facebook
```

### Search Examples
```
search automation testing
find web testing tools
look for python selenium
query best practices
```

### Authentication Examples
```
login username admin password pass123
sign in user john password secret
authenticate username test pass 123
```

### Advanced Examples
```
click button
fill input with data
wait 3 seconds
open youtube and search tutorials
search google then login username user password pass
```

---

## 9. Sample Output

```json
{
  "total_tests": 5,
  "passed": 5,
  "failed": 0,
  "success_rate": "100.0%",
  "details": [
    {
      "action": "Open https://www.google.com",
      "status": "PASS"
    },
    {
      "action": "Page loaded",
      "status": "PASS"
    },
    {
      "action": "Element present: body",
      "status": "PASS"
    },
    {
      "action": "Fill input: input[name='q']",
      "status": "PASS"
    },
    {
      "action": "Press Enter",
      "status": "PASS"
    }
  ]
}
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

## 10. Key Improvements (v2.0 Release)

🆕 **Advanced NLP Engine**
- Regex-based URL detection
- 30+ keyword variations
- Context-aware parsing
- Flexible credential extraction

🆕 **Premium UI**
- Beautiful Streamlit interface
- Live metrics dashboard
- Quick action buttons
- Expandable results
- Clickable links

🆕 **Extended Capabilities**
- Login/authentication support
- Form filling and interaction
- Timing and wait controls
- Multi-step command chains

🆕 **Better Reporting**
- Success rate calculation
- Detailed step information
- Error messages with context
- Tabbed interface

---

## 11. Conclusion

This project demonstrates a complete automated testing workflow using natural language input and browser automation.
It successfully integrates instruction parsing, test execution, and reporting into a single end-to-end system suitable for academic evaluation.

The v2.0 release with advanced NLP capabilities enables users to write tests in natural, conversational language with minimal technical knowledge.

---

## 12. Author

**Ayan Hamdan** - Developer of AI Website Testing Agent

This project was developed as an academic submission to demonstrate the use of natural language processing and browser automation for automated website testing.

The work focuses on converting user-defined natural language instructions into automated Playwright test executions, validating results, and presenting structured pass/fail reports through an integrated system. The project reflects practical understanding of software testing concepts, backend integration, and end-to-end system design.

### Key Contributions:
✅ Advanced NLP with intelligent keyword recognition
✅ Regex-based URL and credential detection
✅ Streamlit UI with metrics and reporting
✅ LangGraph workflow orchestration
✅ Cross-browser Playwright automation
✅ End-to-end test execution pipeline

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

