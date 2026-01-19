# AI Agent for Automated Website Testing Using Natural Language

## 🖼️ UI Screenshots

### Main Application Interface

![Detailed Report](ui%20ss/Screenshot%202026-01-16%20175356.png)
*Natural Language Test Agent Interface*

![Test Execution](ui%20ss/Screenshot%202026-01-17%20095427.png)
*Test Execution with Generated Code*

![Test Results](ui%20ss/Screenshot%202026-01-17%20095442.png)
*Test Results and Reports Display*

### Application Pages

![Home Page](ui%20ss/Screenshot%202026-01-16%20175230.png)
*Application Home Page*

![Login Page](ui%20ss/Screenshot%202026-01-16%20175248%20-%20Copy.png)
*User Login Interface*

![Dashboard](ui%20ss/Screenshot%202026-01-16%20175256.png)
*User Dashboard*

![Test Page](ui%20ss/Screenshot%202026-01-16%20175332.png)
*Static Test Page for Automation*

![Test Reports](ui%20ss/Screenshot%202026-01-16%20175345.png)
*Test Reports View*

*Detailed Test Report Display*

---

## What Was Fixed and Added:

**File Structure**
```
app.py                 - Main Flask application with database integration
templates/
  - login.html        - Fixed and enhanced login page
  - signup.html       - Enhanced signup with email field
  - forgot.html       - Fixed forgot password page
  - dashboard.html    - Enhanced with database info
  - main.html         - Fixed landing page
static/
  - style.css         - Improved styling with all fixes
auth.db               - SQLite database (auto-created)
```

## Test Credentials:

**Username:** admin  
**Password:** 1234

**Username:** user  
**Password:** password123

## Features Now Available:

✓ User Registration with email  
✓ Login with session management  
✓ Password reset feature  
✓ User dashboard with profile info  
✓ Database persistence  
✓ Account creation & login tracking  
✓ Professional UI with modern design  
✓ Mobile responsive layout  
✓ Error handling with user feedback  

## Running the Application:

### Option 1: Simple Launcher (Recommended)
```bash
python run_app.py
```

### Option 2: Direct Flask Run
```bash
python app.py
```

### Option 3: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium

# Run the app
python app.py
```

Access at: http://127.0.0.1:5000  
Agent page: http://127.0.0.1:5000/agent

---

## 🎨 UI Features

The application features a modern, polished interface with:
- **Clean Design** - Professional gradient color scheme (#540863, #92487A, #E49BA6, #FFD3D5)
- **Responsive Layout** - Works seamlessly on desktop and mobile devices
- **Intuitive Navigation** - Easy-to-use interface for test creation and execution
- **Real-time Feedback** - Live status updates during test execution
- **Comprehensive Reports** - Beautiful HTML-formatted test reports with detailed metrics

All errors have been resolved and the application is production-ready with full database support!

## Milestone 1 (Week 1–2) Checklist ✅

- ✅ Flask server with structured templates/static assets
- ✅ Static HTML test page for automation (`/testpage`)
- ✅ Baseline LangGraph agent handling NL inputs (`/agent`)
- ✅ Playwright run wiring (planned for later milestones)

## Milestone 2 (Week 3–4) Checklist ✅

- ✅ **Instruction Parser Module** - Enhanced parser that extracts detailed test case information (action types, targets, values, assertions)
- ✅ **Structured Command Mapping** - Commands mapped to structured format with action_type, target, value, description
- ✅ **LangGraph Workflow** - Parser → Command Mapper → Code Generator workflow established
- ✅ **Code Generation** - Converts structured commands into executable Playwright Python code
- ✅ **Validation** - Test case conversion output validated and displayed in UI

## Milestone 3 (Week 5–6) Checklist ✅

- ✅ **Playwright Code Generation Module** - Enhanced script creation with professional formatting
- ✅ **Assertion Generator** - Comprehensive assertion generator for result validation
- ✅ **Playwright Execution Logic** - Headless browser execution with result capture
- ✅ **Execution Endpoint** - `/execute` API endpoint for running generated tests
- ✅ **Test Runner** - Complete test execution workflow with error handling
- ✅ **Local Form Testing** - Tested sample cases on local HTML forms (`/testpage`)
- ✅ **UI Integration** - Execute button and results display in agent interface

## Milestone 4 (Week 7–8) Checklist ✅

- ✅ **Reporting Module** - Comprehensive test result capture and formatting
 -✅ **Advanced Error Handling** - Intelligent error classification and recovery suggestions
- ✅ **Adaptive DOM Mapping** - Multiple selector strategies for element finding
- ✅ **Polished UI** - Professional test report display with HTML formatting
- ✅ **End-to-End Workflow** - Complete flow from input → parse → generate → execute → report
- ✅ **Reports View** - Dedicated page for viewing all test reports
- ✅ **Final Documentation** - Complete project documentation and examples

## Environment Setup

```bash
python -m venv env
env\Scripts\activate        # Windows
# or source env/bin/activate for Unix
pip install -r requirements.txt
python -m playwright install chromium
python app.py
```

### Key Routes
- `/` landing page
- `/login`, `/signup`, `/forgot`
- `/dashboard`, `/profile`
- `/agent` **Enhanced LangGraph agent** that:
  - Parses natural language test instructions
  - Maps to structured commands
  - Generates Playwright Python code
- `/testpage` static page for Playwright-driven interactions

### Milestone 2 Features

The `/agent` route now provides:
1. **Enhanced Instruction Parser** - Extracts URLs, form fields, actions, assertions from natural language
2. **Structured Commands** - Each command has:
   - `action_type`: navigate, click, fill, submit, assert, wait
   - `target`: selector, URL, or element identifier
   - `value`: input value or expected text
   - `description`: human-readable description
3. **Code Generation** - Automatically generates executable Playwright Python code
4. **UI Display** - Shows parsed actions, structured commands, and generated code

### Example Test Instructions

Try these in `/agent`:

**Login Tests:**
- "Login with admin and check dashboard"
- "Login as user with password password123"
- "Login with admin username and verify redirect to dashboard"

**Search Tests:**
- "Search for 'test' on testpage"
- "Navigate to testpage, search for 'automation' and verify results"
- "Go to testpage, enter 'playwright' in search box, click search button"

**Toggle Tests:**
- "Toggle the switch on testpage and verify status"
- "Go to testpage, click toggle switch, and check that status changed to ON"

**Registration Tests:**
- "Navigate to signup page and register a new user"
- "Go to signup page, fill form and submit"

**Complex Tests:**
- "Login with admin and password 1234, verify dashboard loads, then check profile page"
- "Go to testpage, search for 'test', toggle the switch, and verify both actions completed"

See `example_queries.md` for more examples!

### UI Gallery

<details>
<summary>📸 Click to view more UI screenshots</summary>

![Agent with Test Generation](ui%20ss/Screenshot%202026-01-16%20175332%20-%20Copy.png)
*Agent Interface with Test Code Generation*

![Test Execution Results](ui%20ss/Screenshot%202026-01-16%20175345%20-%20Copy.png)
*Test Execution Results View*

</details>

### Milestone 3 Features

The `/agent` route now includes:
1. **Playwright Execution** - Execute generated tests directly from the UI
2. **Assertion Generator** - Automatic generation of validation assertions
3. **Execution Results** - Real-time test execution results with:
   - Pass/Fail status
   - Execution time
   - Assertion counts
   - Output logs
   - Error messages
4. **Code Validation** - Syntax validation before execution
5. **Test Results** - Detailed execution reports

### Execution Endpoints

- `POST /execute` - Execute generated Playwright test code
  ```json
  {
    "code": "generated playwright code",
    "test_name": "test_automated"
  }
  ```
- `POST /validate-code` - Validate code syntax
  ```json
  {
    "code": "playwright code to validate"
  }
  ```




### test instructions like 

Go to signup page, register a new user, then check that dashboard loads after login.

 ## Test agent response 

## Response
Planned test actions:
1. Navigate to login page
2. Fill username and password
3. Submit form and expect dashboard
4. Open signup page
5. Provide username, email, password
6. Submit form and expect confirmation
These steps can be translated to Playwright code.

## Planned Actions
Navigate to login page
Fill username and password
Submit form and expect dashboard
Open signup page
Provide username, email, password
Submit form and expect confirmation
