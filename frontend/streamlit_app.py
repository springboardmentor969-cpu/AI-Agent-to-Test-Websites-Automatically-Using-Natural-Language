import streamlit as st
import requests

st.set_page_config(page_title="AI Test Automation", layout="centered")

st.title("AI Test Automation (macOS)")

instruction = st.text_area(
    "Enter Test Case",
    height=200,
    placeholder="Open the page, enter email, click submit, verify success"
)

if st.button("Run Test"):
    response = requests.post(
        "http://127.0.0.1:5001/run-test",
        json={"instruction": instruction}
    ).json()

    # Metadata
    st.subheader("Execution Info")
    st.json(response["metadata"])

    # Summary
    st.subheader("Summary")
    st.metric("Total Steps", response["summary"]["total"])
    st.metric("Passed", response["summary"]["passed"])
    st.metric("Failed", response["summary"]["failed"])

    # Steps Table
    st.subheader("Step-by-Step Results")
    st.table(response["steps"])
