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

# --- PREMIUM CYBER-NOIR THEME WITH HOLOGRAPHIC EFFECTS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;600;700&family=Exo+2:wght@400;700;900&family=Share+Tech+Mono&display=swap');
    
    /* Cyber Matrix Background with Animated Grid */
    @keyframes gridPulse {
        0%, 100% { opacity: 0.15; }
        50% { opacity: 0.25; }
    }
    
    @keyframes holographicShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes scanline {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(100vh); }
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a0f2e 50%, #0d1b2a 100%);
        position: relative;
        overflow-x: hidden;
    }
    
    /* Animated Cyber Grid Overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px),
            linear-gradient(rgba(255, 0, 255, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 0, 255, 0.05) 1px, transparent 1px);
        background-size: 100px 100px, 100px 100px, 20px 20px, 20px 20px;
        background-position: 0 0, 0 0, 0 0, 0 0;
        animation: gridPulse 4s ease-in-out infinite;
        z-index: 0;
        pointer-events: none;
    }
    
    /* Holographic Scanline Effect */
    .stApp::after {
        content: "";
        position: fixed;
        top: -100%;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(0, 255, 255, 0.5) 50%, 
            transparent 100%);
        animation: scanline 8s linear infinite;
        z-index: 1;
        pointer-events: none;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
    }

    /* Premium Cyber Typography */
    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif;
        color: #e0f2ff;
        letter-spacing: 0.5px;
    }

    /* Holographic Title with Glitch Effect */
    @keyframes glitchText {
        0% { text-shadow: 0 0 20px rgba(0, 255, 255, 0.8), 0 0 40px rgba(255, 0, 255, 0.6); }
        25% { text-shadow: -2px 0 rgba(0, 255, 255, 0.8), 2px 0 rgba(255, 0, 255, 0.6); }
        50% { text-shadow: 0 0 30px rgba(0, 255, 255, 0.9), 0 0 50px rgba(255, 0, 255, 0.7); }
        75% { text-shadow: 2px 0 rgba(0, 255, 255, 0.8), -2px 0 rgba(255, 0, 255, 0.6); }
        100% { text-shadow: 0 0 20px rgba(0, 255, 255, 0.8), 0 0 40px rgba(255, 0, 255, 0.6); }
    }
    
    .neon-title {
        font-family: 'Exo 2', sans-serif;
        font-weight: 900;
        font-size: 3.5rem !important;
        text-transform: uppercase;
        letter-spacing: 6px;
        background: linear-gradient(135deg, #00ffff 0%, #ff00ff 50%, #00ffff 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: holographicShift 3s ease infinite, glitchText 5s ease-in-out infinite;
        margin: 0;
        padding-top: 10px;
        filter: drop-shadow(0 0 15px rgba(0, 255, 255, 0.6));
    }

    /* HUD-Style Glass Cards with Holographic Border */
    @keyframes borderGlow {
        0%, 100% { border-color: rgba(0, 255, 255, 0.4); box-shadow: 0 0 20px rgba(0, 255, 255, 0.2); }
        50% { border-color: rgba(255, 0, 255, 0.6); box-shadow: 0 0 30px rgba(255, 0, 255, 0.3); }
    }
    
    .glass-card {
        background: linear-gradient(135deg, rgba(10, 14, 26, 0.85) 0%, rgba(26, 15, 46, 0.85) 100%);
        backdrop-filter: blur(30px) saturate(180%);
        border: 2px solid rgba(0, 255, 255, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    /* Corner Brackets for HUD Effect */
    .glass-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            #00ffff 25%, 
            #ff00ff 50%, 
            #00ffff 75%, 
            transparent 100%);
        animation: borderGlow 3s ease-in-out infinite;
    }
    
    .glass-card::after {
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 30px; height: 30px;
        border-top: 3px solid #00ffff;
        border-left: 3px solid #00ffff;
        border-radius: 20px 0 0 0;
        opacity: 0.6;
    }
    
    .glass-card:hover {
        border-color: rgba(0, 255, 255, 0.7);
        background: linear-gradient(135deg, rgba(10, 14, 26, 0.95) 0%, rgba(26, 15, 46, 0.95) 100%);
        box-shadow: 
            0 0 40px rgba(0, 255, 255, 0.4),
            0 0 60px rgba(255, 0, 255, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transform: translateY(-3px) scale(1.01);
    }

    /* Cyber Neon Buttons with Pulse Effect */
    @keyframes buttonPulse {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.4); }
        50% { box-shadow: 0 0 30px rgba(0, 255, 255, 0.7), 0 0 50px rgba(255, 0, 255, 0.5); }
    }
    
    .stButton button {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 50%, #f21170 100%) !important;
        background-size: 200% 200% !important;
        color: #fff !important;
        border: 2px solid rgba(0, 255, 255, 0.5) !important;
        border-radius: 15px !important;
        font-family: 'Exo 2', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        transition: all 0.4s ease !important;
        height: 60px !important;
        margin-top: 15px !important;
        position: relative !important;
        overflow: hidden !important;
        animation: buttonPulse 3s ease-in-out infinite;
    }
    
    .stButton button::before {
        content: "" !important;
        position: absolute !important;
        top: 0 !important; left: -100% !important;
        width: 100% !important; height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent) !important;
        transition: left 0.5s !important;
    }
    
    .stButton button:hover::before {
        left: 100% !important;
    }
    
    .stButton button:hover {
        box-shadow: 
            0 0 40px rgba(0, 255, 255, 0.8),
            0 0 60px rgba(255, 0, 255, 0.6),
            inset 0 0 20px rgba(255, 255, 255, 0.2) !important;
        transform: scale(1.05) translateY(-3px) !important;
        border-color: rgba(255, 0, 255, 0.8) !important;
        background-position: 100% 100% !important;
    }

    /* Navigation Tabs with Cyber Style */
    .stButton button[kind="secondary"] {
        background: rgba(0, 20, 40, 0.6) !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
        color: #00ffff !important;
        animation: none !important;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.2) !important;
    }
    
    .stButton button[kind="secondary"]:hover {
        background: rgba(0, 20, 40, 0.8) !important;
        border-color: rgba(0, 255, 255, 0.6) !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5) !important;
    }
    
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%) !important;
        border-color: rgba(0, 255, 255, 0.8) !important;
    }

    /* Holographic Input Fields */
    .stTextArea textarea {
        background: rgba(0, 10, 20, 0.7) !important;
        border: 2px solid rgba(0, 255, 255, 0.4) !important;
        color: #00ffff !important;
        border-radius: 15px !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 1.1rem !important;
        box-shadow: 
            inset 0 0 20px rgba(0, 255, 255, 0.1),
            0 0 15px rgba(0, 255, 255, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: rgba(255, 0, 255, 0.6) !important;
        box-shadow: 
            inset 0 0 30px rgba(0, 255, 255, 0.2),
            0 0 25px rgba(0, 255, 255, 0.4),
            0 0 40px rgba(255, 0, 255, 0.3) !important;
        background: rgba(0, 10, 20, 0.9) !important;
    }
    
    /* Toggle Switch Cyber Style */
    .stCheckbox, .stToggle {
        color: #00ffff !important;
    }

    /* Hide standard UI elements */
    [data-testid="stHeader"] { visibility: hidden; pointer-events: none; }
    [data-testid="stSidebar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
    
    /* Cyber Scrollbar */
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { 
        background: #0a0e1a; 
        border-left: 1px solid rgba(0, 255, 255, 0.2);
    }
    ::-webkit-scrollbar-thumb { 
        background: linear-gradient(180deg, #00ffff 0%, #ff00ff 100%); 
        border-radius: 10px; 
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }
    ::-webkit-scrollbar-thumb:hover { 
        background: linear-gradient(180deg, #00d4ff 0%, #f21170 100%);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
    }
    
    /* Expander Cyber Style */
    .streamlit-expanderHeader {
        background: rgba(0, 20, 40, 0.5) !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        color: #00ffff !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: rgba(0, 255, 255, 0.6) !important;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.3) !important;
    }
    
    /* Success/Error Messages Cyber Style */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 12px !important;
        border-left: 4px solid !important;
    }
    
    .stSuccess {
        background: rgba(0, 255, 136, 0.1) !important;
        border-left-color: #00ff88 !important;
        color: #00ff88 !important;
    }
    
    .stError {
        background: rgba(255, 0, 100, 0.1) !important;
        border-left-color: #ff0064 !important;
        color: #ff0064 !important;
    }
    
    .stWarning {
        background: rgba(255, 200, 0, 0.1) !important;
        border-left-color: #ffc800 !important;
        color: #ffc800 !important;
    }
    
    .stInfo {
        background: rgba(0, 200, 255, 0.1) !important;
        border-left-color: #00c8ff !important;
        color: #00c8ff !important;
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
    st.markdown('<h1 class="neon-title">AI WEB TESTING AGENT</h1>', unsafe_allow_html=True)

with header_col2:
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    headless = st.toggle("BACKGROUND MODE", value=True, help="Run browser without visual window")

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Custom Navigation (Replaces st.tabs for programmatic control)
nav_col1, nav_col2, _ = st.columns([1, 1, 3])
with nav_col1:
    if st.button("🚀 START TESTING", use_container_width=True, type="primary" if st.session_state.active_tab == "start" else "secondary"):
        st.session_state.active_tab = "start"
        st.rerun()
with nav_col2:
    if st.button("📋 VIEW RESULTS", use_container_width=True, type="primary" if st.session_state.active_tab == "results" else "secondary"):
        st.session_state.active_tab = "results"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.active_tab == "start":
    st.markdown("""
    <div class="glass-card">
        <h3 style="margin-top:0; font-family:'Exo 2', sans-serif; font-size:1.3rem; color:#00ffff; margin-bottom:0; text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);">⚡ ENTER YOUR TESTING PROTOCOL</h3>
    </div>
    """, unsafe_allow_html=True)
    
    instructions = st.text_area(
        "Enter your steps", 
        height=180,
        placeholder="Go to https://google.com then search for 'AI Testing'",
        value=st.session_state.get("draft_instructions", ""),
        label_visibility="collapsed"
    )
    
    col_btn, _ = st.columns([1, 2])
    with col_btn:
        run_btn = st.button("RUN  NOW")

    if run_btn:
        tests = [line.strip() for line in instructions.split("\n") if line.strip()]
        
        if not tests:
            st.warning("Please enter at least one step.")
        else:
            with st.status("🤖 GETTING THE AGENT READY...", expanded=True) as status:
                st.write("📖 Reading your steps...")
                graph = build_batch_graph()
                app = graph.compile()
                
                st.write("🏃 Testing the website...")
                
                settings = {
                    "headless": headless,
                    "timeout": timeout
                }
                
                result = app.invoke({
                    "instructions": tests,
                    "settings": settings
                })
                
                status.update(label="🎉 ALL TESTS FINISHED!", state="complete", expanded=False)

            st.session_state.last_result = result
            st.session_state.active_tab = "results" # REDIRECT TO RESULTS
            st.rerun()

elif st.session_state.active_tab == "results":
    if "last_result" in st.session_state:
        reports = st.session_state.last_result.get("reports", [])
        exec_results = st.session_state.last_result.get("exec_results", [])
        
        # --- SUMMARY DASHBOARD ---
        total_tasks = len(exec_results)
        success_count = sum(1 for r in exec_results if r.get("success", False))
        issue_count = total_tasks - success_count
        
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px;">
            <div class="glass-card" style="text-align: center; border-left: 5px solid #00ffff; box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);">
                <p style="color: #00ffff; font-size: 0.7rem; text-transform: uppercase; letter-spacing:3px; font-weight:700; margin-bottom:8px; font-family:'Exo 2';">📊 TOTAL OPERATIONS</p>
                <h2 style="margin: 0; font-size: 2.5rem; font-family:'Exo 2'; font-weight:900; color:#00ffff; text-shadow: 0 0 15px rgba(0, 255, 255, 0.6);">{total_tasks}</h2>
            </div>
            <div class="glass-card" style="text-align: center; border-left: 5px solid #00ff88; box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);">
                <p style="color: #00ff88; font-size: 0.7rem; text-transform: uppercase; letter-spacing:3px; font-weight:700; margin-bottom:8px; font-family:'Exo 2';">✅ SUCCESS RATE</p>
                <h2 style="margin: 0; font-size: 2.5rem; color: #00ff88; font-family:'Exo 2'; font-weight:900; text-shadow: 0 0 15px rgba(0, 255, 136, 0.6);">{int((success_count/total_tasks)*100) if total_tasks > 0 else 0}%</h2>
            </div>
            <div class="glass-card" style="text-align: center; border-left: 5px solid #ff0064; box-shadow: 0 0 20px rgba(255, 0, 100, 0.2);">
                <p style="color: #ff0064; font-size: 0.7rem; text-transform: uppercase; letter-spacing:3px; font-weight:700; margin-bottom:8px; font-family:'Exo 2';">⚠️ ANOMALIES</p>
                <h2 style="margin: 0; font-size: 2.5rem; color: #ff0064; font-family:'Exo 2'; font-weight:900; text-shadow: 0 0 15px rgba(255, 0, 100, 0.6);">{issue_count}</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        for i, (rep, exec_res) in enumerate(zip(reports, exec_results)):
            success = exec_res.get("success", False)
            logs = exec_res.get("logs", [])
            screenshots = exec_res.get("screenshots", [])
            video_path = exec_res.get("video")
            html_report_path = rep['html_report']
            
            with st.container():
                # HEADER CARD
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(0, 15, 30, 0.8), rgba(10, 0, 20, 0.8)); border-left: 5px solid {'#00ff88' if success else '#ff0064'}; padding: 25px; border-radius: 15px; margin-bottom: 25px; backdrop-filter: blur(20px); box-shadow: 0 0 30px {'rgba(0, 255, 136, 0.3)' if success else 'rgba(255, 0, 100, 0.3)'};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin: 0; color: #00ffff; font-family:'Exo 2'; letter-spacing:2px; font-size: 1.3rem; text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);">⚡ TEST PROTOCOL #{i+1}</h3>
                        <span style="background: {'rgba(0, 255, 136, 0.15)' if success else 'rgba(255, 0, 100, 0.15)'}; color: {'#00ff88' if success else '#ff0064'}; padding: 8px 20px; border-radius: 20px; font-size: 0.8rem; font-weight: 800; border: 2px solid {'#00ff88' if success else '#ff0064'}; letter-spacing:2px; font-family:'Exo 2'; box-shadow: 0 0 15px {'rgba(0, 255, 136, 0.4)' if success else 'rgba(255, 0, 100, 0.4)'};">
                            {'✓ PASSED' if success else '✗ FAILED'}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # MAIN CONTENT COLUMNS
                col_left, col_right = st.columns([1.2, 1], gap="medium")
                
                with col_left:
                    st.markdown("<h4 style='font-family:Exo 2; font-size:1rem; color:#00ffff; margin-bottom:15px; text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);'>� EXECUTION LOGS</h4>", unsafe_allow_html=True)
                    with st.expander("SEE STEP-BY-STEP LOGS", expanded=not success):
                        for log in logs:
                            if "[ERROR]" in log or "FAILED" in log:
                                st.error(log)
                            elif "[OK]" in log:
                                st.success(log)
                            elif "[WAIT]" in log or "[HEAL]" in log or "[AI" in log:
                                st.warning(log)
                            else:
                                st.info(log)
                    
                    st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
                    
                    # ACTION BUTTONS
                    btn_col1, btn_col2 = st.columns([1, 1])
                    with btn_col1:
                        if os.path.exists(html_report_path):
                            with open(html_report_path, "rb") as f:
                                st.download_button(
                                    label="🌐 DOWNLOAD HTML",
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
                                    label="📥 DOWNLOAD PDF",
                                    data=f,
                                    file_name=os.path.basename(pdf_path),
                                    mime="application/pdf",
                                    key=f"dl_pdf_{i}",
                                    use_container_width=True
                                )
                    
                    # INTEGRATED HTML VIEWER (ALWAYS SHOWN)
                    st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
                    if os.path.exists(html_report_path):
                        with open(html_report_path, "r", encoding="utf-8") as f:
                            html_content = f.read()
                        st.components.v1.html(html_content, height=500, scrolling=True)
                    else:
                        st.error("Extended report file missing.")

                with col_right:
                    st.markdown("<h4 style='font-family:Exo 2; font-size:1rem; color:#00ffff; margin-bottom:15px; text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);'>� VISUAL DATA</h4>", unsafe_allow_html=True)
                    
                    if screenshots:
                        cols_sc = st.columns(len(screenshots) if len(screenshots) < 3 else 3)
                        for idx, sc in enumerate(screenshots):
                            if idx < 3 and os.path.exists(sc):
                                with cols_sc[idx % len(cols_sc)]:
                                    st.image(sc, use_container_width=True, caption=f"Capture {idx+1}")
                    
                    if video_path and os.path.exists(video_path):
                        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                        st.markdown("<p style='font-size:0.85rem; color:#00ffff; font-family:Exo 2; text-shadow: 0 0 8px rgba(0, 255, 255, 0.4);'>🎬 VIDEO PLAYBACK</p>", unsafe_allow_html=True)
                        st.video(video_path)
                    elif not screenshots:
                        st.info("No visual data collected for this test.")
                
                st.markdown("<div style='height:60px; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom:40px;'></div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:100px 0;">
            <p style="color:#00ffff; font-family:'Exo 2'; font-size:1.1rem; text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);">⚠️ NO DATA AVAILABLE • INITIATE TESTING PROTOCOL</p>
        </div>
        """, unsafe_allow_html=True)
