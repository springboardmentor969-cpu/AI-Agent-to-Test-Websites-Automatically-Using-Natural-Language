from typing import TypedDict, List, Dict, Any
import json
import os
from datetime import datetime
from langgraph.graph import StateGraph, START, END

from codegen import generate_playwright_test
from runner import run_generated_test


LOGIN_URL = "http://127.0.0.1:5000/login"


class AgentState(TypedDict):
    instruction: str
    steps: List[Dict[str, Any]]
    code_path: str
    report: Dict[str, Any]   


try:
    from langchain_groq import ChatGroq
    from langchain_core.prompts import ChatPromptTemplate
except Exception:
    ChatGroq = None
    ChatPromptTemplate = None


llm = None
if ChatGroq and os.getenv("GROQ_API_KEY"):
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)



def parse_instruction_llm(state: AgentState) -> AgentState:
    instruction = state["instruction"]
    steps = None

    if llm and ChatPromptTemplate:
        try:
            prompt = ChatPromptTemplate.from_template(
                """
Convert instruction into JSON Playwright steps.
Target page: {url}

Allowed actions:
goto(url), fill(selector,value), click(selector), assert_text(selector,value)

Return ONLY JSON.

Instruction: "{instruction}"
"""
            )

            res = (prompt | llm).invoke({
                "instruction": instruction,
                "url": LOGIN_URL
            })
            steps = json.loads(res.content.strip())
        except Exception:
            steps = None

    if steps is None:
        steps = _simple_parse_instruction(instruction)

    steps = [s for s in steps if isinstance(s, dict) and "action" in s]

    if not any(s["action"] == "goto" for s in steps):
        steps.insert(0, {"action": "goto", "url": LOGIN_URL})

    state["steps"] = steps
    return state


def _simple_parse_instruction(instruction: str):
    import re

    instr = instruction.lower()
    steps = [{"action": "goto", "url": LOGIN_URL}]

    if m := re.search(r"username\s+(\w+)", instr):
        steps.append({"action": "fill", "selector": "#username", "value": m.group(1)})

    if m := re.search(r"password\s+(\w+)", instr):
        steps.append({"action": "fill", "selector": "#password", "value": m.group(1)})

    if "login" in instr:
        steps.append({"action": "click", "selector": "#login-button"})

    if m := re.search(r"(welcome|success|error|invalid)", instr):
        steps.append({
            "action": "assert_text",
            "selector": "#message",
            "value": m.group(1).capitalize()
        })

    return steps



def code_generation_node(state: AgentState) -> AgentState:
    path = "generated_tests/test_generated.py"
    generate_playwright_test(state["steps"], path)
    state["code_path"] = path
    return state



def execution_node(state: AgentState) -> AgentState:
    state["report"] = run_generated_test(state["code_path"])
    return state



workflow = StateGraph(AgentState)

workflow.add_node("parse", parse_instruction_llm)
workflow.add_node("codegen", code_generation_node)
workflow.add_node("execute", execution_node)

workflow.add_edge(START, "parse")
workflow.add_edge("parse", "codegen")
workflow.add_edge("codegen", "execute")
workflow.add_edge("execute", END)

app = workflow.compile()



def run_test_cycle(instruction: str) -> Dict[str, Any]:
    final_state = app.invoke({
        "instruction": instruction,
        "steps": [],
        "code_path": "",
        "report": {}
    })

    return {
        "instruction": instruction,
        "llm_used": llm is not None,
        "parsed_steps": final_state["steps"],
        "generated_test_file": final_state["code_path"],
        "execution": final_state["report"],
        "timestamp": datetime.now().isoformat()
    }
