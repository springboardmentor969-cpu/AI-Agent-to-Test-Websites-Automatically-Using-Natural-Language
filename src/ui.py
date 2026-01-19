import streamlit as st
from workflow import execute_workflow

st.set_page_config(
    page_title="AI Website Testing Agent",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Website Testing Agent")
st.caption("Automated testing using Natural Language, LangGraph & Playwright")

instruction = st.text_input(
    "Enter Test Instruction",
    placeholder="open google | search automation testing"
)

if st.button("🚀 Run Test"):
    if not instruction.strip():
        st.warning("Please enter a test instruction")
    else:
        with st.spinner("Running automated test in headless mode..."):
            report = execute_workflow(instruction)

        st.success("Test Completed")

        st.write("Total Steps:", report["total"])
        st.write("Passed:", report["passed"])
        st.write("Failed:", report["failed"])

        st.markdown("---")

        for step in report["details"]:
            if step["status"] == "PASS":
                st.success(f"PASS → {step['action']}")
            else:
                st.error(f"FAIL → {step['action']}")
