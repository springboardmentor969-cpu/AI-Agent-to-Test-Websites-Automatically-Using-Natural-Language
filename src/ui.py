import streamlit as st
import requests
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Website Testing Agent",
    page_icon="🤖",
    layout="centered"
)

# ---------------- TITLE ----------------
st.title("🤖 AI Website Testing Agent")
st.caption("Automated E2E Testing using Natural Language & Playwright")

# ---------------- INPUT ----------------
instruction = st.text_input(
    "Enter Test Instruction",
    placeholder="Example: open google or search automation"
)

# ---------------- RUN BUTTON ----------------
if st.button("🚀 Run Test"):
    if not instruction.strip():
        st.warning("Please enter a test instruction")
    else:
        with st.spinner("Executing AI-powered testing pipeline..."):
            time.sleep(0.5)

            try:
                response = requests.post(
                    "http://127.0.0.1:5000/run",
                    json={"instruction": instruction},
                    timeout=60
                )

                result = response.json()

            except Exception as e:
                st.error(f"Backend connection failed: {e}")
                st.stop()

        # ---------------- RESULT DISPLAY ----------------
        st.success("✅ Test completed successfully")
        st.subheader("📊 Test Report")

        # SAFE extraction (NO KeyError possible)
        details = result.get("details", [])
        total = result.get("total_tests", len(details))
        passed = result.get("passed", 0)
        failed = result.get("failed", 0)

        st.write("Total Steps:", total)
        st.write("Passed:", passed)
        st.write("Failed:", failed)

        st.markdown("---")

        # Show step-by-step results
        if not details:
            st.info("No detailed steps returned by backend.")
        else:
            for item in details:
                action = item.get("action", "Unknown action")
                status = item.get("status", "UNKNOWN")

                if status == "PASS":
                    st.success(f"PASS → {action}")
                elif status == "FAIL":
                    st.error(f"FAIL → {action}")
                else:
                    st.warning(f"{status} → {action}")
