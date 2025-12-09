import streamlit as st
import pandas as pd
import random
from app_backend.theme import apply_cyber_theme, render_sidebar
from app_backend.incidents import load_incidents
from app_backend.tickets import load_tickets
from app_backend.datasets import load_datasets

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

apply_cyber_theme()
render_sidebar()

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first.")
    st.stop()

role = st.session_state.get("role", "analyst")

# ================== HEADER ==================
st.markdown("""
<div class="header-bar">
  <div><strong>Future Icon SOC • Live Threat Overview</strong></div>
  <div class="terminal-typing">
    Ingesting cyber incidents, IT tickets and dataset signals in real time...
  </div>
</div>
""", unsafe_allow_html=True)

st.title("📊 Cyber Intelligence Dashboard")

# ================== LOAD DATA ==================
inc = load_incidents()
tickets = load_tickets()
datasets = load_datasets()

# ================== KPI METRICS ==================
c1, c2, c3 = st.columns(3)
c1.metric("Total Incidents", len(inc))
c2.metric("Total Tickets", len(tickets))
c3.metric("Datasets", len(datasets))

high_critical = inc[inc["severity"].isin(["High", "Critical"])].shape[0] if "severity" in inc.columns else 0
open_tickets = tickets[tickets["status"] == "Open"].shape[0] if "status" in tickets.columns else 0

if high_critical > 0:
    st.error(f"🚨 {high_critical} High/Critical incidents require attention.")
if open_tickets > 0:
    st.warning(f"📥 {open_tickets} IT tickets are still open.")

st.divider()

# ================== HUD / HOLOGRAM SECTION ==================
st.subheader("🛰 Holographic System HUD")

h1, h2, h3 = st.columns(3)
with h1:
    st.markdown("""
    <div class="hud-circle">
        <div class="hud-label">
            <b>Incidents</b><br/>
            Realtime<br/>
        </div>
    </div>
    """, unsafe_allow_html=True)

with h2:
    st.markdown("""
    <div class="hud-circle">
        <div class="hud-label">
            <b>Tickets</b><br/>
            Support load<br/>
        </div>
    </div>
    """, unsafe_allow_html=True)

with h3:
    st.markdown("""
    <div class="hud-circle">
        <div class="hud-label">
            <b>Datasets</b><br/>
            Intelligence feeds<br/>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ================== NETWORK GRAPH ==================
st.subheader("🌐 Network Graph (Logical View)")

graph_dot = """
digraph G {
  rankdir=LR;
  node [shape=circle, style=filled, color="#00ff9d", fontcolor="black"];
  Internet -> Firewall;
  Firewall -> WebGateway;
  Firewall -> AppServer;
  AppServer -> Database;
  WebGateway -> Users;
}
"""

st.graphviz_chart(graph_dot)

st.divider()

# ================== RADAR SCANNER + MAP ==================
col_radar, col_map = st.columns(2)

with col_radar:
    st.subheader("📡 Radar Scanner")
    st.markdown("""
    <div class="radar-wrapper">
      <div class="radar-grid"></div>
      <div class="radar-beam"></div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Rotating radar visual to show scanning activity (decorative).")

with col_map:
    st.subheader("🗺 Global SOC Nodes (Sample)")
    map_df = pd.DataFrame(
        [
            {"lat": 25.276987, "lon": 55.296249},  # Dubai
            {"lat": 51.507351, "lon": -0.127758},  # London
            {"lat": 40.712776, "lon": -74.005974}, # New York
            {"lat": 35.689487, "lon": 139.691711}, # Tokyo
        ]
    )
    st.map(map_df, zoom=1)

st.divider()

# ================== THREAT FEED ==================
st.subheader("⚡ Real-Time Threat Feed (Simulated)")

threat_types = ["Phishing", "Ransomware", "DDoS", "Bruteforce", "Data Exfiltration"]
regions = ["EMEA", "APAC", "NA", "LATAM"]
assets = ["Email Gateway", "Web Server", "Database Cluster", "VPN Gateway", "User Endpoint"]

def generate_fake_threats(n=6):
    rows = []
    for _ in range(n):
        t = random.choice(threat_types)
        r = random.choice(regions)
        a = random.choice(assets)
        sev = random.choice(["Low", "Medium", "High", "Critical"])
        rows.append(f"- [{sev}] {t} targeting **{a}** in **{r}**")
    return rows

if st.button("🔄 Refresh Threat Feed"):
    st.session_state.threat_feed = generate_fake_threats()

feed = st.session_state.get("threat_feed") or generate_fake_threats()
for line in feed:
    st.markdown(line)

st.divider()

# ================== BASIC ANALYTICS ==================
st.subheader("📈 Incident & Ticket Analytics")

a1, a2 = st.columns(2)
with a1:
    st.markdown("**Incidents by Severity**")
    if "severity" in inc.columns and not inc.empty:
        st.bar_chart(inc["severity"].value_counts())
    else:
        st.info("No severity data available.")

with a2:
    st.markdown("**Tickets by Status**")
    if "status" in tickets.columns and not tickets.empty:
        st.bar_chart(tickets["status"].value_counts())
    else:
        st.info("No ticket status data available.")

if role == "admin":
    st.subheader("📊 Datasets by Source (Admin Only)")
    if "source" in datasets.columns and not datasets.empty:
        st.bar_chart(datasets["source"].value_counts())
    else:
        st.info("No dataset source data available.")
