import streamlit as st

def apply_cyber_theme():
    st.markdown("""
    <style>

    /* =======================
       MATRIX ANIMATED BACKGROUND
       ======================= */
    body {
        background: black !important;
        overflow-x: hidden !important;
    }

    @keyframes matrixMove {
        0% { background-position: 0 0; }
        100% { background-position: 0 4000px; }
    }

    .stApp:before {
        content: "";
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-image: url('https://i.imgur.com/1J4CYVq.png');  /* soft matrix code */
        opacity: 0.1;
        z-index: -1;
        animation: matrixMove 60s linear infinite;
    }

    /* =============================
       NEON GLOWING OUTER BORDER
       ============================= */
    .stApp {
        border: 3px solid rgba(0,255,157,0.5);
        border-radius: 15px;
        box-shadow: 0 0 25px rgba(0,255,157,0.55);
        padding: 8px;
        margin: 6px;
        color: #00ff9d !important;
        font-family: "Consolas","Fira Code",monospace !important;
    }

    /* =============================
       TYPOGRAPHY & HEADERS
       ============================= */
    h1, h2, h3, h4 {
        color: #00ff9d !important;
        text-shadow: 0px 0px 14px rgba(0,255,157,0.9);
    }

    @keyframes matrixGlow {
        0% { text-shadow: 0 0 6px #00ff9d; }
        50% { text-shadow: 0 0 20px #00ff9d; }
        100% { text-shadow: 0 0 6px #00ff9d; }
    }

    h1 {
        animation: matrixGlow 3s infinite ease-in-out;
    }

    /* =============================
       3D NEON BUTTONS
       ============================= */
    .stButton > button {
        background: rgba(0,255,157,0.15);
        border: 1px solid rgba(0,255,157,0.6);
        border-radius: 12px;
        color: #00ff9d;
        padding: 10px 20px;
        font-weight: bold;
        transition: 0.25s;
        transform: perspective(350px) translateZ(0px);
    }

    .stButton > button:hover {
        background: rgba(0,255,157,0.35);
        box-shadow: 0 0 20px rgba(0,255,157,0.9);
        transform: perspective(350px) translateZ(16px);
        color: black;
    }

    /* =============================
       INPUTS / TEXTBOXES
       ============================= */
    input, textarea, select {
        background: rgba(0,255,157,0.08) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(0,255,157,0.30) !important;
        color: #00ff9d !important;
        box-shadow: none !important;
    }

    input:focus, textarea:focus, select:focus {
        border-color: rgba(0,255,157,0.6) !important;
        background: rgba(0,255,157,0.15) !important;
        box-shadow: 0 0 10px rgba(0,255,157,0.6) !important;
        outline: none !important;
    }

    /* Remove random grey containers */
    .css-1d391kg, .css-1cpxqw2 {
        background: transparent !important;
        box-shadow: none !important;
    }

    /* ============================
       TABLE STYLING
       ============================ */
    [data-testid="stDataFrame"] {
        border-radius: 13px !important;
        border: 1px solid rgba(0,255,157,0.3) !important;
        box-shadow: 0 0 25px rgba(0,255,157,0.25) !important;
        overflow: hidden !important;
    }
    .dataframe thead th {
        background: rgba(0,255,157,0.25) !important;
        color: #00ff9d !important;
        font-weight: bold;
    }
    .dataframe tbody tr:hover {
        background: rgba(0,255,157,0.18) !important;
    }

    /* ============================
       TABS
       ============================ */
    .stTabs [data-baseweb="tab"] {
        background: rgba(0,255,157,0.1);
        border-radius: 10px;
        margin-right: 8px;
        border: 1px solid rgba(0,255,157,0.4);
    }
    .stTabs [aria-selected="true"] {
        background: rgba(0,255,157,0.5) !important;
        color: black !important;
        box-shadow: 0 0 12px rgba(0,255,157,0.9);
        font-weight: bold;
    }

    /* ============================
       GLOWING HEADER BAR
       ============================ */
    .header-bar {
        margin-top: 5px;
        margin-bottom: 10px;
        padding: 10px 16px;
        border-radius: 12px;
        border: 1px solid rgba(0,255,157,0.55);
        background: linear-gradient(90deg, rgba(0,255,157,0.15), transparent);
        box-shadow: 0 0 18px rgba(0,255,157,0.7);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* TERMINAL TYPING ANIMATION */
    .terminal-typing {
        font-family: "Fira Code","Consolas",monospace;
        font-size: 13px;
        white-space: nowrap;
        overflow: hidden;
        border-right: 2px solid #00ff9d;
        width: 0;
        animation: typing 7s steps(60, end) infinite alternate,
                   caret 0.8s steps(1,end) infinite;
    }
    @keyframes typing {
        from { width: 0; }
        to   { width: 100%; }
    }
    @keyframes caret {
        0%, 100% { border-color: transparent; }
        50% { border-color: #00ff9d; }
    }

    /* ============================
       HUD CIRCLES / HOLOGRAM
       ============================ */
    .hud-circle {
        position: relative;
        width: 140px;
        height: 140px;
        margin: auto;
        border-radius: 50%;
        border: 2px solid rgba(0,255,157,0.7);
        box-shadow: 0 0 15px rgba(0,255,157,0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: visible;
    }

    .hud-circle::before,
    .hud-circle::after {
        content: "";
        position: absolute;
        border-radius: 50%;
        border: 1px dashed rgba(0,255,157,0.7);
    }

    .hud-circle::before {
        width: 110px;
        height: 110px;
        animation: spinOuter 14s linear infinite;
    }
    .hud-circle::after {
        width: 70px;
        height: 70px;
        animation: spinInner 9s linear infinite reverse;
    }

    @keyframes spinOuter {
        from { transform: rotate(0deg); }
        to   { transform: rotate(360deg); }
    }

    @keyframes spinInner {
        from { transform: rotate(360deg); }
        to   { transform: rotate(0deg); }
    }

    .hud-label {
        font-size: 12px;
        text-align: center;
    }

    /* ============================
       RADAR SCANNER
       ============================ */
    .radar-wrapper {
        position: relative;
        width: 220px;
        height: 220px;
        margin: auto;
        border-radius: 50%;
        border: 2px solid rgba(0,255,157,0.7);
        box-shadow: 0 0 18px rgba(0,255,157,0.9);
        overflow: hidden;
    }

    .radar-grid {
        position: absolute;
        inset: 10px;
        border-radius: 50%;
        border: 1px solid rgba(0,255,157,0.4);
    }
    .radar-grid::before,
    .radar-grid::after {
        content: "";
        position: absolute;
        background: rgba(0,255,157,0.25);
    }
    .radar-grid::before {
        width: 2px;
        height: 100%;
        left: 50%; top: 0;
    }
    .radar-grid::after {
        height: 2px;
        width: 100%;
        left: 0; top: 50%;
    }

    .radar-beam {
        position: absolute;
        width: 50%;
        height: 2px;
        top: 50%;
        left: 50%;
        transform-origin: left center;
        background: linear-gradient(90deg, rgba(0,255,157,0.9), transparent);
        animation: sweep 3s linear infinite;
    }

    @keyframes sweep {
        from { transform: rotate(0deg); }
        to   { transform: rotate(360deg); }
    }

    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Sidebar with neon SVG logo & user info."""
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; margin-bottom: 10px;">
        <svg width="110" height="110" viewBox="0 0 200 200">
          <defs>
            <filter id="glow">
              <feGaussianBlur stdDeviation="4" result="blur"/>
              <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>
          <path d="M100 15 L180 60 L180 145 L100 185 L20 145 L20 60 Z"
                stroke="#00ff9d" stroke-width="5" fill="none" filter="url(#glow)"/>
          <circle cx="100" cy="100" r="35"
                stroke="#00ff9d" stroke-width="5" fill="none" filter="url(#glow)"/>
        </svg>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🧬 Future Icon SOC")
        st.caption("Cyber Intelligence Command Center")

        if "username" in st.session_state:
            st.markdown(f"**User:** `{st.session_state.username}`")
        if "role" in st.session_state:
            st.markdown(f"**Role:** `{st.session_state.role}`")
