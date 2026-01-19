import streamlit as st
from workflow import execute_workflow

st.set_page_config(
    page_title="AI Website Testing Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Website Testing Agent")
st.caption("🚀 Convert Natural Language to Automated Web Tests | Powered by NLP + LangGraph + Playwright")

# Sidebar with comprehensive instructions
with st.sidebar:
    st.header("📖 NLP Command Examples")
    st.markdown("""
    ### 🌐 Navigation
    - **open google**
    - **visit github.com**
    - **go to https://example.com**
    - **open youtube**
    - **navigate to facebook**
    
    ### 🔍 Search
    - **search automation testing**
    - **find web testing tools**
    - **look for python selenium**
    - **query best practices**
    
    ### 🔐 Authentication
    - **login username admin password pass123**
    - **sign in user john password secret**
    - **authenticate username test pass 123**
    
    ### ⚡ Advanced Actions
    - **click button**
    - **fill input with test data**
    - **wait 5 seconds**
    - **press enter**
    
    ### 🎯 Combined Actions
    - **go to google and search automation**
    - **visit example.com then login username user pass 123**
    
    ### 💡 Tips
    ✅ Type naturally in conversational language
    ✅ URLs are auto-detected and converted to links
    ✅ Credentials are extracted automatically
    ✅ Works with any website domain
    """)

# Main content
col1, col2 = st.columns([3, 1])

with col1:
    instruction = st.text_input(
        "Enter Test Instruction (NLP Powered)",
        placeholder="Example: open google and search test automation",
        help="Type in natural language and let AI convert it to test steps"
    )

with col2:
    run_button = st.button("🚀 Run Test", use_container_width=True, type="primary")

# Quick example buttons
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📱 Open Google", use_container_width=True):
        instruction = "open google"
        run_button = True

with col2:
    if st.button("🔍 Search Test", use_container_width=True):
        instruction = "search automation testing"
        run_button = True

with col3:
    if st.button("🔐 Login Demo", use_container_width=True):
        instruction = "login username testuser password Test@123"
        run_button = True

with col4:
    if st.button("🌐 Custom URL", use_container_width=True):
        instruction = "open github.com"
        run_button = True

# Main execution
if run_button or instruction:
    if not instruction.strip():
        st.warning("⚠️ Please enter a test instruction")
    else:
        st.markdown("---")
        with st.spinner("🔄 Converting NLP to test steps and executing..."):
            try:
                report = execute_workflow(instruction)
                st.success("✅ Test completed successfully!")

                # Display metrics in beautiful cards
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("📊 Total Tests", report["total_tests"], delta=None)
                with col2:
                    st.metric("✅ Passed", report["passed"], delta=None)
                with col3:
                    st.metric("❌ Failed", report["failed"], delta=None)
                with col4:
                    success_rate = report.get("success_rate", "0%")
                    st.metric("📈 Success Rate", success_rate, delta=None)

                # Display detailed report with better formatting
                st.subheader("📊 Detailed Test Report")
                
                # Create tabs for different sections
                tab1, tab2 = st.tabs(["Test Results", "Raw JSON"])
                
                with tab1:
                    for idx, detail in enumerate(report["details"], 1):
                        status_icon = "✅" if detail["status"] == "PASS" else "❌"
                        
                        with st.expander(f"{status_icon} Step {idx}: {detail['action']}", expanded=(idx == 1)):
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                if detail["status"] == "PASS":
                                    st.success(f"**Status:** PASS")
                                else:
                                    st.error(f"**Status:** FAIL")
                                    if "error" in detail:
                                        st.code(detail["error"], language="python")
                            
                            with col2:
                                st.metric("Step", idx)
                            
                            # Add clickable links for URLs
                            if "http" in detail.get("action", "").lower():
                                url = detail["action"].split("Open ")[-1] if "Open" in detail["action"] else ""
                                if url.startswith("http"):
                                    st.markdown(f"**🔗 [Click to Open Link]({url})**")
                
                with tab2:
                    st.json(report)

            except Exception as e:
                st.error("❌ Execution failed")
                st.exception(e)
