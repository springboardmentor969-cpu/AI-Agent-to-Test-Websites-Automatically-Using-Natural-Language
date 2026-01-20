# 🤖 AI Agent for Automated Website Testing

This project implements an intelligent agent that performs automated end-to-end (E2E) testing on web applications using natural language instructions.

## ✨ Features

- **Natural Language Parsing**: Accepts human-readable test instructions
- **Automated Test Execution**: Uses Playwright for headless browser automation
- **Dynamic Assertion Generation**: Automatically generates validation checks
- **AI-Powered Selector Healing**: Uses Grok (xAI) to fix broken selectors automatically
- **Real-time Execution Logs**: Live monitoring of test execution
- **Screenshot Capture**: Automatic screenshots on test failures
- **Modern Web UI**: Beautiful interface with dark mode and progress indicators
- **AI Agent Integration**: Optional LangChain integration with GPT-4 for complex interactions
- **Comprehensive Reporting**: Detailed test reports with logs and evidence

## 🎯 AI Agent Modes

### Custom Agent (Default)
- Uses custom natural language parsing
- Supports structured commands like "open youtube", "enter value field"
- AI selector healing with Grok (optional)
- No API key required for basic functionality
- Fast execution with smart waits

### LangChain AI Agent
- Uses GPT-4 for intelligent command interpretation
- Supports complex, conversational instructions
- Requires OpenAI API key
- Currently provides toolkit information (full agent integration in development)

## 🚀 Installation

1. **Clone and setup**:
   ```bash
   git clone <your-repo-url>
   cd ai-agent-nl
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**:
   ```bash
   playwright install
   ```

4. **Configure API keys** (Optional):
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## 🔧 Configuration

### Environment Variables (.env)
```env
# For AI Selector Healing (Optional)
GROK_API_KEY=your_grok_api_key_here

# For LangChain AI Agent (Optional)
OPENAI_API_KEY=your_openai_api_key_here
```

## 🎮 Usage

1. **Start the Flask server**:
   ```bash
   python main.py
   ```

2. **Open your browser** to `http://127.0.0.1:5000`

3. **Try these reliable test instructions**:
   - ✅ `"open google, search for python"` (Fast & reliable)
   - ✅ `"open github, search for machine learning"` (Fast & reliable)
   - ⚠️ `"open youtube, search for ai tutorials"` (May be slow/heavy)
   - ✅ `"open login page, enter john username, enter password123 password, click login"`

4. **Choose execution mode**:
   - Custom Agent: Fast, structured parsing
   - AI Agent: Intelligent interpretation (requires OpenAI key)

### **Tips for Success:**
- **Google & GitHub** work best for quick testing
- **Social media sites** (YouTube, Facebook) may be slow or blocked
- **Use simple instructions** for best results
- **Check your internet connection** for timeouts
   - `"open login page, enter john username, enter password123 password, click login"`

4. **Choose execution mode**:
   - Custom Agent: Fast, structured parsing
   - AI Agent: Intelligent interpretation (requires OpenAI key)

## 📝 Example Instructions

**Basic Navigation:**
```
open google, search for python testing
```

**Search Operations:**
```
open google, search for python
open youtube, search for machine learning
```

**Form Interaction:**
```
open login page, enter john username, enter password123 password, click login button
```

**Complex Scenarios:**
```
navigate to youtube, search for ai tutorials, click first video, verify video is playing
```

## 🎨 UI Features

- **🌙 Dark Mode**: Toggle between light and dark themes
- **📊 Progress Indicators**: Real-time execution progress
- **📜 Live Logs**: Terminal-style execution logs
- **📸 Screenshot Gallery**: View captured screenshots
- **📱 Responsive Design**: Works on desktop and mobile
- **⚡ Modern Interface**: Smooth animations and transitions

## 🏗️ Architecture

```
src/
├── agent.py              # LangGraph workflow orchestration
├── instruction_parser/   # Natural language parsing
├── assertion_generator/  # Automatic test assertions
├── playwright_executor/  # Browser automation execution
├── reporting/           # Test report generation
├── ai_selector.py       # AI-powered selector healing
└── smart_waits.py       # Intelligent waiting strategies
```

## 📝 Example Instructions

**Basic Navigation:**
```
open google, search for python testing
```

**Form Interaction:**
```
open login page, enter john username, enter password123 password, click login button
```

**Complex Scenarios:**
```
navigate to youtube, search for ai tutorials, click first video, verify video is playing
```

## 🔍 AI Selector Healing

When selectors fail, the system automatically:
1. Tries alternative CSS selectors
2. Uses fuzzy DOM scanning
3. Calls Grok AI to analyze the HTML and suggest correct selectors
4. Falls back gracefully if AI is unavailable

## 📊 Reporting

Test results include:
- ✅ Execution status and timing
- 📋 Detailed action logs
- 🔍 Assertion results
- 📸 Failure screenshots
- 🎥 Video recordings (when enabled)
- 📄 JSON export for CI/CD integration

2. Open your browser and navigate to `http://127.0.0.1:5000`

3. Enter natural language instructions, e.g.:
   - "open login page, enter mahi in username, enter 1234 in password, click login"

4. Click "Run Agent" to execute the test

## Supported Instructions

- Navigate: "open login page", "open youtube", "open google"
- Fill fields: "enter value in field"
- Click elements: "click element"
- Assertions: Automatically generated based on actions

## Project Structure

- `main.py`: Flask server entry point
- `src/agent.py`: LangGraph agent workflow
- `src/instruction_parser/`: Parses natural language to actions
- `src/assertion_generator/`: Generates test assertions
- `src/playwright_executor/`: Executes tests in browser
- `src/reporting/`: Generates test reports
- `static/`: HTML pages for UI

## Running Tests

Run unit tests:
```bash
python -m unittest discover tests/
```

## Demo

To run a full end-to-end test:
1. Start the server: `python main.py`
2. Open browser to `http://127.0.0.1:5000`
3. Enter instruction: "open login page, enter mahi in username, enter 1234 in password, click login"
4. The agent will execute the test and display results

## Supported Actions

- **Navigate**: open youtube, open google, open login page
- **Fill**: enter value in field (username, password)
- **Click**: click element (login)
- **Wait**: wait for element
- **Assert**: verify/assert text presence

## Assertions Generated

- URL contains check after navigation
- Field value verification after fill
- Text presence check for assert actions
- Custom checks based on actions