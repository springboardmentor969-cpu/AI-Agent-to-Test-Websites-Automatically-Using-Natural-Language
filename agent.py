import os
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

from src.instruction_parser.instruction_parser import InstructionParser
from src.assertion_generator.assertion_generator import AssertionGenerator


# -----------------------------
# Agent State Definition
# -----------------------------
class AgentState(TypedDict):
    instruction: str
    actions: List[dict]
    assertions: List[dict]


# -----------------------------
# Node 1: Parse Instruction
# -----------------------------
def parse_instruction(state: AgentState) -> AgentState:
    parser = InstructionParser()
    actions = parser.parse(state["instruction"])

    # 🔥 IMPORTANT FIX: convert local HTML to file:/// URL
    for action in actions:
        if action.get("action") == "navigate":
            if "login.html" in action.get("url", ""):
                base_dir = os.getcwd()
                login_path = os.path.join(
                    base_dir, "static", "login.html"
                )

                file_url = "file:///" + login_path.replace("\\", "/")
                action["url"] = file_url

    return {
        "instruction": state["instruction"],
        "actions": actions,
        "assertions": []
    }


# -----------------------------
# Node 2: Generate Assertions
# -----------------------------
def generate_assertions(state: AgentState) -> AgentState:
    assertion_generator = AssertionGenerator()
    assertions = assertion_generator.generate(state["actions"])

    return {
        "instruction": state["instruction"],
        "actions": state["actions"],
        "assertions": assertions
    }


# -----------------------------
# Create LangGraph Agent
# -----------------------------
def create_agent():
    workflow = StateGraph(AgentState)

    workflow.add_node("parse_instruction", parse_instruction)
    workflow.add_node("generate_assertions", generate_assertions)

    workflow.set_entry_point("parse_instruction")
    workflow.add_edge("parse_instruction", "generate_assertions")
    workflow.add_edge("generate_assertions", END)

    return workflow.compile()


# -----------------------------
# Agent Instance
# -----------------------------
agent = create_agent()
