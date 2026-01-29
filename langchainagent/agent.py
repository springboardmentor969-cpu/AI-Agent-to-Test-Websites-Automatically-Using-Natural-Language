import os
import re
import uuid
import ast
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# ================= ENV =================
load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
AUTO_EXECUTE = os.getenv("AUTO_EXECUTE", "true").lower() == "true"
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

if not HF_API_TOKEN:
    raise RuntimeError("HF_API_TOKEN missing")

llm = InferenceClient(
    model="Qwen/Qwen2.5-Coder-7B-Instruct",
    token=HF_API_TOKEN
)

# ================= PATHS =================
BASE = Path.cwd()
TESTS = BASE / "generated_tests"
ART = BASE / "artifacts"
SHOTS = ART / "screenshots"
VIDS = ART / "videos"
MEMORY_FILE = BASE / "site_memory.json"

for d in [TESTS, SHOTS, VIDS]:
    d.mkdir(parents=True, exist_ok=True)

if not MEMORY_FILE.exists():
    MEMORY_FILE.write_text("{}")

# ================= MEMORY =================
def load_memory():
    return json.loads(MEMORY_FILE.read_text())

def save_memory(mem):
    MEMORY_FILE.write_text(json.dumps(mem, indent=2))

# ================= DEFAULT SITE MODELS =================
DEFAULT_SITES = {
    "youtube": {
        "search_input": "input[name='search_query']",
        "results": "ytd-video-renderer",
        "spa": True
    },
    "wikipedia": {
        "search_input": "input[name='search']",
        "results": "#mw-content-text",
        "spa": False
    }
}

# ================= PARSER =================
def parse_instruction(text):
    t = text.lower().strip()
    m = re.match(r"open\s+(\w+)\s+and\s+search\s+for\s+(.+)", t)
    if m:
        return "open_and_search", m.group(1), m.group(2)
    m = re.match(r"open\s+(\w+)", t)
    if m:
        return "open", m.group(1), None
    raise ValueError("Unsupported instruction")

# ================= URL RESOLUTION =================
def candidate_urls(site):
    return [
        f"https://{site}.com",
        f"https://www.{site}.com"
    ]

# ================= SCRIPT GENERATOR =================
def generate_script(intent, site, query):
    headless = "True" if HEADLESS else "False"
    memory = load_memory()
    site_cfg = memory.get(site) or DEFAULT_SITES.get(site)

    code = [
        "from playwright.sync_api import sync_playwright",
        "",
        "def run():",
        f"    with sync_playwright() as p:",
        f"        browser = p.chromium.launch(headless={headless})",
        f"        context = browser.new_context(record_video_dir=r\"{VIDS}\")",
        f"        page = context.new_page()",
    ]

    # ---- Direct navigation
    code.append("        for url in [")
    for u in candidate_urls(site):
        code.append(f"            \"{u}\",")
    code.append("        ]:")
    code.append("            try:")
    code.append("                page.goto(url, wait_until='domcontentloaded', timeout=8000)")
    code.append("                break")
    code.append("            except:")
    code.append("                pass")
    code.append("        else:")
    code.append("            page.goto('https://www.google.com')")
    code.append(f"            page.fill(\"input[name='q']\", \"{site}\")")
    code.append("            page.press(\"input[name='q']\", 'Enter')")
    code.append("            page.wait_for_selector('h3')")
    code.append("            page.locator('h3').first.click()")

    code.append("        page.wait_for_load_state('networkidle')")
    code.append("        page.wait_for_timeout(1500)")

    # ---- Search workflow
    if intent == "open_and_search" and site_cfg:
        si = site_cfg["search_input"]
        res = site_cfg["results"]

        code.extend([
            f"        page.wait_for_selector(\"{si}\")",
            f"        page.click(\"{si}\")",
            f"        page.fill(\"{si}\", {query!r})",
            f"        with page.expect_navigation():",
            f"            page.press(\"{si}\", 'Enter')",
            "        page.wait_for_load_state('networkidle')",
            "        page.wait_for_timeout(2000)",
            f"        page.wait_for_selector(\"{res}\")",
            f"        assert \"{query.lower()}\" in page.content().lower()",
        ])

        # ---- Multi-tab workflow (open first result)
        code.extend([
            f"        results = page.locator(\"{res}\")",
            "        if results.count() > 0:",
            "            with context.expect_page() as p2:",
            "                results.first.click()",
            "            tab = p2.value",
            "            tab.wait_for_load_state('networkidle')",
            f"            tab.screenshot(path=r\"{SHOTS / 'detail.png'}\")",
            "            tab.close()",
        ])

    # ---- Finalize
    code.extend([
        f"        page.screenshot(path=r\"{SHOTS / 'final.png'}\")",
        "        context.close()",
        "        browser.close()",
        "",
        "if __name__ == '__main__':",
        "    run()",
    ])

    return "\n".join(code)

# ================= MEMORY UPDATE =================
def update_memory(site, success, site_cfg):
    if not success or not site_cfg:
        return
    mem = load_memory()
    mem[site] = site_cfg
    save_memory(mem)

# ================= MAIN AGENT =================
def run_agent(user_input):
    intent, site, query = parse_instruction(user_input)
    script = generate_script(intent, site, query)

    # ---- LLM refinement (safe)
    try:
        resp = llm.conversational(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Refine Playwright Python code. "
                        "Do not remove logic. Output only Python."
                    ),
                },
                {"role": "user", "content": script},
            ],
            max_new_tokens=300,
        )
        refined = resp["choices"][0]["message"]["content"]
        ast.parse(refined)
        script = refined
    except Exception:
        pass

    path = TESTS / f"test_{uuid.uuid4().hex[:8]}.py"
    path.write_text(script, encoding="utf-8")

    success = True
    if AUTO_EXECUTE:
        try:
            subprocess.run(["python", str(path)], check=True)
        except Exception:
            success = False

    update_memory(site, success, DEFAULT_SITES.get(site))

    return {
        "script": str(path),
        "screenshots": [str(SHOTS / "final.png"), str(SHOTS / "detail.png")],
        "videos": str(VIDS),
        "memory": str(MEMORY_FILE),
    }