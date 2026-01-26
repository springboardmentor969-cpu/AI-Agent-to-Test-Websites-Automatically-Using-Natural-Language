import sys
import os
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from agent.graph_batch import build_batch_graph

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Agent For Web Testing",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- CYBERPUNK TERMINAL CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;600;800&display=swap');
    
    /* Dark Terminal Background with Scanlines */
    .stApp {
        background: #0a0a0f;
        background-image: 
            repeating-linear-gradient(
                0deg,
                rgba(0, 255, 136, 0.03) 0px,
                rgba(0, 255, 136, 0.03) 1px,
                transparent 1px,
                transparent 2px
            );
        background-attachment: fixed;
    }
    
    /* Animated Grid Overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: 
            linear-gradient(90deg, rgba(0, 255, 136, 0.02) 1px, transparent 1px),
            linear-gradient(rgba(0, 255, 136, 0.02) 1px, transparent 1px);
        background-size: 80px 80px;
        pointer-events: none;
        z-index: 0;
    }
    
    /* Corner Glow Effect */
    .stApp::after {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: 
            radial-gradient(ellipse at 0% 0%, rgba(0, 255, 136, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 100% 100%, rgba(0, 200, 255, 0.06) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }

    /* Typography */
    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif;
        color: #e0e0e0;
        letter-spacing: 0.02em;
    }

    /* Main Title - Glitch Style */
    .cyber-header {
        font-family: 'Share Tech Mono', monospace;
        font-size: 2.6rem !important;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 6px;
        color: #00ff88;
        text-shadow: 
            0 0 10px rgba(0, 255, 136, 0.8),
            0 0 20px rgba(0, 255, 136, 0.4),
            0 0 40px rgba(0, 255, 136, 0.2),
            2px 2px 0px #00c8ff;
        margin: 0;
        padding: 15px 0;
        position: relative;
    }
    
    .cyber-header::before {
        content: ">";
        margin-right: 15px;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }

    /* Terminal Cards - Angular Design */
    .terminal-card {
        background: linear-gradient(135deg, rgba(0, 20, 15, 0.9) 0%, rgba(10, 10, 20, 0.95) 100%);
        border: 1px solid #00ff88;
        border-left: 4px solid #00ff88;
        padding: 1.5rem;
        margin-bottom: 1rem;
        position: relative;
        clip-path: polygon(0 0, calc(100% - 15px) 0, 100% 15px, 100% 100%, 15px 100%, 0 calc(100% - 15px));
        box-shadow: 
            0 0 15px rgba(0, 255, 136, 0.15),
            inset 0 0 30px rgba(0, 255, 136, 0.03);
        transition: all 0.3s ease;
    }
    
    .terminal-card:hover {
        border-color: #00c8ff;
        box-shadow: 
            0 0 25px rgba(0, 200, 255, 0.25),
            inset 0 0 40px rgba(0, 200, 255, 0.05);
    }
    
    .terminal-card::before {
        content: "";
        position: absolute;
        top: 0; right: 0;
        width: 15px; height: 15px;
        background: #00ff88;
        clip-path: polygon(100% 0, 0 100%, 100% 100%);
    }
    
    .terminal-card::after {
        content: "SYS://";
        position: absolute;
        top: 8px; right: 25px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.6rem;
        color: #00ff88;
        opacity: 0.5;
    }

    /* Neon Buttons */
    .stButton button {
        background: transparent !important;
        color: #00ff88 !important;
        border: 2px solid #00ff88 !important;
        border-radius: 0 !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-weight: 400 !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        transition: all 0.3s !important;
        height: 50px !important;
        margin-top: 10px !important;
        clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
        position: relative;
        overflow: hidden;
    }
    
    .stButton button::before {
        content: "";
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 136, 0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton button:hover {
        background: rgba(0, 255, 136, 0.15) !important;
        box-shadow: 
            0 0 20px rgba(0, 255, 136, 0.5),
            inset 0 0 20px rgba(0, 255, 136, 0.1) !important;
        transform: translateY(-2px);
    }
    
    .stButton button:hover::before {
        left: 100%;
    }

    /* Active/Primary Button State */
    .stButton button[kind="primary"] {
        background: rgba(0, 255, 136, 0.2) !important;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.3) !important;
    }
    
    .stButton button[kind="secondary"] {
        border-color: #00c8ff !important;
        color: #00c8ff !important;
    }
    
    .stButton button[kind="secondary"]:hover {
        background: rgba(0, 200, 255, 0.15) !important;
        box-shadow: 0 0 20px rgba(0, 200, 255, 0.5) !important;
    }

    /* Text Input - Terminal Style */
    .stTextArea textarea {
        background: rgba(0, 10, 8, 0.8) !important;
        border: 1px solid #00ff8855 !important;
        border-left: 3px solid #00ff88 !important;
        color: #00ff88 !important;
        border-radius: 0 !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.95rem !important;
        padding: 15px !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #00ff8866 !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #00c8ff !important;
        box-shadow: 0 0 15px rgba(0, 200, 255, 0.2) !important;
    }

    /* Toggle Switch */
    .stToggle label {
        font-family: 'Share Tech Mono', monospace !important;
        color: #00c8ff !important;
        font-size: 0.75rem !important;
        letter-spacing: 2px !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(0, 20, 15, 0.6) !important;
        border: 1px solid #00ff8844 !important;
        border-radius: 0 !important;
        color: #00ff88 !important;
        font-family: 'Share Tech Mono', monospace !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(0, 10, 8, 0.6) !important;
        border: 1px solid #00ff8833 !important;
        border-top: none !important;
    }

    /* Status Messages */
    .stSuccess, .stInfo, .stWarning, .stError {
        background: rgba(0, 10, 8, 0.8) !important;
        border-radius: 0 !important;
        font-family: 'Share Tech Mono', monospace !important;
    }

    /* Hide Streamlit Elements */
    [data-testid="stHeader"] { visibility: hidden; pointer-events: none; }
    [data-testid="stSidebar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0a0a0f; }
    ::-webkit-scrollbar-thumb { background: #00ff88; }
    ::-webkit-scrollbar-thumb:hover { background: #00c8ff; }
    
    /* Stats Cards */
    .stat-box {
        background: linear-gradient(180deg, rgba(0, 20, 15, 0.9) 0%, rgba(5, 15, 12, 0.95) 100%);
        border: 1px solid;
        padding: 20px;
        text-align: center;
        position: relative;
        clip-path: polygon(0 10px, 10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%);
    }
    
    .stat-box::before {
        content: "";
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 2px;
        background: currentColor;
        opacity: 0.5;
    }
    
    .stat-label {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 8px;
        opacity: 0.8;
    }
    
    .stat-value {
        font-family: 'Exo 2', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 0 20px currentColor;
    }
    
    /* Section Headers */
    .section-title {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.85rem;
        color: #00c8ff;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 15px;
        padding-left: 15px;
        border-left: 3px solid #00c8ff;
    }
    
    /* Test Result Header */
    .result-header {
        background: linear-gradient(90deg, rgba(0, 20, 15, 0.9) 0%, transparent 100%);
        padding: 18px 25px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
    }
    
    .result-header::before {
        content: "";
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 4px;
    }
    
    .result-title {
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.1rem;
        letter-spacing: 2px;
        margin: 0;
        color: #fff;
    }
    
    .status-badge {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.7rem;
        padding: 6px 18px;
        letter-spacing: 2px;
        text-transform: uppercase;
        clip-path: polygon(8px 0, 100% 0, calc(100% - 8px) 100%, 0 100%);
    }
    </style>
""", unsafe_allow_html=True)

# --- INTERNAL SETTINGS ---
timeout = 10000

# Initialize navigation state
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "start"

# --- MAIN CONTENT ---
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown('<h1 class="cyber-header">AI_WEB_TEST.AGENT</h1>', unsafe_allow_html=True)

with header_col2:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    headless = st.toggle("STEALTH MODE", value=True, help="Run browser without visual window")

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# Custom Navigation
nav_col1, nav_col2, _ = st.columns([1, 1, 3])
with nav_col1:
    if st.button("[ INITIALIZE TEST ]", use_container_width=True, type="primary" if st.session_state.active_tab == "start" else "secondary"):
        st.session_state.active_tab = "start"
        st.rerun()
with nav_col2:
    if st.button("[ VIEW LOGS ]", use_container_width=True, type="primary" if st.session_state.active_tab == "results" else "secondary"):
        st.session_state.active_tab = "results"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.active_tab == "start":
    st.markdown("""
    <div class="terminal-card">
        <p style="margin:0; font-family:'Share Tech Mono', monospace; font-size:0.9rem; color:#00ff88;">
            <span style="color:#00c8ff;">[INPUT]</span> ENTER TEST SEQUENCE BELOW_
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    instructions = st.text_area(
        "Enter your steps", 
        height=160,
        placeholder="> navigate to https://amazon.in\n> search for 'iPhone pro max'\n> select first result\n> add to cart",
        value=st.session_state.get("draft_instructions", ""),
        label_visibility="collapsed"
    )
    
    col_btn, _ = st.columns([1, 2])
    with col_btn:
        run_btn = st.button(">>> EXECUTE")

    if run_btn:
        instructions_text = instructions.strip()
        
        if not instructions_text:
            st.warning("⚠ NO INSTRUCTIONS DETECTED")
        else:
            tests = [instructions_text]

            with st.status("◉ INITIALIZING AGENT...", expanded=True) as status:
                st.write("◈ Parsing instructions...")
                graph = build_batch_graph()
                app = graph.compile()
                
                st.write("◈ Executing test sequence...")
                
                settings = {
                    "headless": headless,
                    "timeout": timeout
                }
                
                result = app.invoke({
                    "instructions": tests,
                    "settings": settings
                })
                
                status.update(label="◉ SEQUENCE COMPLETE", state="complete", expanded=False)

            st.session_state.last_result = result
            st.session_state.active_tab = "results"
            st.rerun()

elif st.session_state.active_tab == "results":
    if "last_result" in st.session_state:
        reports = st.session_state.last_result.get("reports", [])
        exec_results = st.session_state.last_result.get("exec_results", [])
        
        # --- STATS DASHBOARD ---
        total_tasks = len(exec_results)
        success_count = sum(1 for r in exec_results if r.get("success", False))
        issue_count = total_tasks - success_count
        success_rate = int((success_count/total_tasks)*100) if total_tasks > 0 else 0
        
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px;">
            <div class="stat-box" style="border-color: #00c8ff; color: #00c8ff;">
                <p class="stat-label">◆ OPERATIONS</p>
                <h2 class="stat-value">{total_tasks}</h2>
            </div>
            <div class="stat-box" style="border-color: #00ff88; color: #00ff88;">
                <p class="stat-label">◆ SUCCESS RATE</p>
                <h2 class="stat-value">{success_rate}%</h2>
            </div>
            <div class="stat-box" style="border-color: #ff3366; color: #ff3366;">
                <p class="stat-label">◆ FAILURES</p>
                <h2 class="stat-value">{issue_count}</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        for i, (rep, exec_res) in enumerate(zip(reports, exec_results)):
            success = exec_res.get("success", False)
            logs = exec_res.get("logs", [])
            screenshots = exec_res.get("screenshots", [])
            video_path = exec_res.get("video")
            html_report_path = rep['html_report']
            
            status_color = "#00ff88" if success else "#ff3366"
            status_text = "PASSED" if success else "FAILED"
            
            with st.container():
                st.markdown(f"""
                <div class="result-header" style="border-left-color: {status_color};">
                    <h3 class="result-title">TEST_CASE_{i+1:02d}</h3>
                    <span class="status-badge" style="background: {status_color}22; color: {status_color}; border: 1px solid {status_color};">
                        {status_text}
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
                col_left, col_right = st.columns([1.2, 1], gap="medium")
                
                with col_left:
                    st.markdown('<p class="section-title">◈ EXECUTION LOG</p>', unsafe_allow_html=True)
                    with st.expander("EXPAND TRACE DATA", expanded=not success):
                        for log in logs:
                            if "[ERROR]" in log or "FAILED" in log:
                                st.error(f"✗ {log}")
                            elif "[OK]" in log:
                                st.success(f"✓ {log}")
                            elif "[WAIT]" in log or "[HEAL]" in log or "[AI" in log:
                                st.warning(f"◉ {log}")
                            else:
                                st.info(f"→ {log}")
                    
                    st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
                    
                    btn_col1, btn_col2 = st.columns([1, 1])
                    with btn_col1:
                        if os.path.exists(html_report_path):
                            with open(html_report_path, "rb") as f:
                                st.download_button(
                                    label="↓ HTML REPORT",
                                    data=f,
                                    file_name=os.path.basename(html_report_path),
                                    mime="text/html",
                                    key=f"dl_html_{i}",
                                    use_container_width=True
                                )
                    
                    with btn_col2:
                        pdf_path = rep.get("pdf_report")
                        if pdf_path and os.path.exists(pdf_path):
                            with open(pdf_path, "rb") as f:
                                st.download_button(
                                    label="↓ PDF REPORT",
                                    data=f,
                                    file_name=os.path.basename(pdf_path),
                                    mime="application/pdf",
                                    key=f"dl_pdf_{i}",
                                    use_container_width=True
                                )
                    
                    st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
                    if os.path.exists(html_report_path):
                        with open(html_report_path, "r", encoding="utf-8") as f:
                            html_content = f.read()
                        st.components.v1.html(html_content, height=500, scrolling=True)
                    else:
                        st.error("◉ REPORT FILE NOT FOUND")

                with col_right:
                    st.markdown('<p class="section-title">◈ VISUAL DATA</p>', unsafe_allow_html=True)
                    
                    if screenshots:
                        cols_sc = st.columns(len(screenshots) if len(screenshots) < 3 else 3)
                        for idx, sc in enumerate(screenshots):
                            if idx < 3 and os.path.exists(sc):
                                with cols_sc[idx % len(cols_sc)]:
                                    st.image(sc, use_container_width=True, caption=f"FRAME_{idx+1:02d}")
                    
                    if video_path and os.path.exists(video_path):
                        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                        st.markdown("<p style='font-size:0.75rem; color:#00c8ff; font-family:\"Share Tech Mono\", monospace;'>▶ VIDEO CAPTURE</p>", unsafe_allow_html=True)
                        st.video(video_path)
                    elif not screenshots:
                        st.info("◉ NO VISUAL DATA CAPTURED")
                
                st.markdown("<div style='height:50px; border-bottom: 1px solid #00ff8833; margin-bottom:40px;'></div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="terminal-card" style="text-align:center; padding:80px 0;">
            <p style="color:#00ff8888; font-family:'Share Tech Mono', monospace; font-size:1rem;">
                [ NO DATA ]<br><br>
                <span style="font-size:0.8rem; opacity:0.6;">Execute a test sequence to view results</span>
            </p>
        </div>
        """, unsafe_allow_html=True)