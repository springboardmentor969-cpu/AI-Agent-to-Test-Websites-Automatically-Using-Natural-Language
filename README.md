# AI Agent to Test Websites Automatically Using Natural Language

A Hybrid Rule-Based + LLM-Refined Testing System
## 📌 Overview

This project is an intelligent web automation agent that converts natural language instructions into executable browser automation scripts.

Instead of relying entirely on a Large Language Model (LLM), the system uses a hybrid approach:

    A rule-based core ensures reliability and correctness

    A lightweight LLM refinement step improves robustness and adaptability

The agent can:

    Open any website (Google, YouTube, Wikipedia, Reddit, or local sites)

    Navigate between sites automatically

    Perform searches inside target websites

    Interact with forms (login, signup, inputs)

    Execute scripts automatically using Playwright

    Capture screenshots and videos

    Run in interactive or CI/headless mode

## ✨ Key Features
🔹 Natural Language Control

Examples of supported instructions:

    open youtube

    open youtube and search for cats

    open wikipedia and search for quantum mechanics

    open http://127.0.0.1:5001 and create account

    open reddit

🔹 Hybrid Agent Architecture

    Rule-based planner (default, deterministic, safe)

    LLM refinement layer (optional, improves selectors and waits)

    Prevents hallucinated or invalid automation code

🔹 Universal Site Support

    Works with any public website

    Works with local development servers

    Does not hardcode Google / Wikipedia / YouTube only

    Automatically detects when to:

        Open a site directly

        Discover a site via Google

        Search inside the site

🔹 Automatic Execution

    Generated scripts are executed automatically

    Uses Chromium via Playwright

    Captures:

        📸 Screenshots

        🎥 Videos (optional)

    Errors are surfaced clearly to the UI

🔹 CI & Headless Mode

    Can run in:

        Interactive browser mode

        Headless CI pipelines

    Suitable for regression testing

## ⚙️ How the System Works (High Level)

    User enters a natural language instruction

    Agent parses intent

        Action (open, search, create, login)

        Target site

        Optional query or task

    Rule-based planner generates a base script

    LLM refines the script (optional)

        Improves selectors

        Adds resilience

    Script is validated

    Playwright executes the script

    Artifacts are saved

    Results are returned to the UI

## 🧠 Why Hybrid (Rule-Based + LLM)?

Approach	                                                   Problem

Pure LLM	                                                   Hallucinates selectors, unstable

Pure rules	                                                   Too rigid, site-specific

Hybrid (this project)	                                       ✅ Reliable + adaptable

This design ensures:

    Deterministic execution

    Better debugging

    Safer automation

    Lower LLM cost

## 🚀 Installation & Setup
1️⃣ Clone the repository

git clone 
cd project

2️⃣ Create a virtual environment (recommended)

python -m venv venv
venv\Scripts\activate

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Install Playwright browsers

playwright install

5️⃣ Create .env file

HF_TOKEN=hf_your_token_here
AUTO_EXECUTE=true
HEADLESS=false

⚠️ One variable per line
⚠️ No quotes

python app.py

Then open:

http://127.0.0.1:5000
