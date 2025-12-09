# pages/3_AI_Assistant.py

import streamlit as st
from google import genai
import pandas as pd

from app_backend.theme import apply_cyber_theme, render_sidebar
from app_backend.incidents import load_incidents
from app_backend.tickets import load_tickets
from app_backend.datasets import load_datasets

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# --------------- THEME + SIDEBAR ------------- #
apply_cyber_theme()
render_sidebar()

# ---------------- LOGIN CHECK ---------------- #
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Login required.")
    st.stop()

username = st.session_state.get("username", "User")
role = st.session_state.get("role", "analyst")

st.title("🤖 Your AI Friend & Cyber Buddy")

st.caption(
    "Chat with a friendly but smart AI. It knows you as the logged-in user and can also "
    "use data from your Cyber Intelligence Portal (incidents, tickets, datasets) when you "
    "ask about them."
)

st.markdown("---")

# --------------- GEMINI CLIENT --------------- #
@st.cache_resource
def get_gemini_client():
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing in .streamlit/secrets.toml"
        )
    return genai.Client(api_key=api_key)

client = None
error_msg = None
try:
    client = get_gemini_client()
except Exception as e:
    error_msg = str(e)
    st.error(f"⚠️ Gemini client error: {e}")

# --------------- LOAD PORTAL DATA ------------ #
@st.cache_data
def fetch_portal_data():
    incidents_df = None
    tickets_df = None
    datasets_df = None
    errors = []

    try:
        incidents_df = load_incidents()
    except Exception as e:
        errors.append(f"Incidents error: {e}")

    try:
        tickets_df = load_tickets()
    except Exception as e:
        errors.append(f"Tickets error: {e}")

    try:
        datasets_df = load_datasets()
    except Exception as e:
        errors.append(f"Datasets error: {e}")

    return incidents_df, tickets_df, datasets_df, errors


incidents_df, tickets_df, datasets_df, data_errors = fetch_portal_data()

if data_errors:
    with st.expander("⚠️ Data load warnings"):
        for err in data_errors:
            st.write("- " + err)

# --------------- SESSION CHAT HISTORY -------- #
if "ai_chat" not in st.session_state:
    st.session_state.ai_chat = [
        {
            "role": "assistant",
            "content": (
                f"Hey **{username}** 👋\n\n"
                "I’m your friendly AI buddy — smart, chill and a bit geeky.\n\n"
                "You can ask me **anything**:\n"
                "- Coding, tech, cybersecurity\n"
                "- Music, life, uni, ideas, business\n"
                "- Or questions about your incidents, tickets and datasets\n"
            ),
        }
    ]

messages = st.session_state.ai_chat


# --------------- DATA CONTEXT BUILDER -------- #
def build_data_context(user_question: str) -> str:
    """
    Build a text summary of relevant portal data based on the user question.
    This does NOT expose raw tables, just aggregates and descriptions.
    """
    if not user_question:
        return ""

    q = user_question.lower()
    lines = []

    # ---- INCIDENTS CONTEXT ----
    if incidents_df is not None and isinstance(incidents_df, pd.DataFrame):
        if any(k in q for k in ["incident", "severity", "breach", "attack", "soc"]):
            lines.append("INCIDENTS SUMMARY:")
            lines.append(f"- Total incidents: {len(incidents_df)}")

            if "severity" in incidents_df.columns:
                sev_counts = incidents_df["severity"].value_counts().to_dict()
                lines.append(f"- Incidents by severity: {sev_counts}")

            if "status" in incidents_df.columns:
                status_counts = incidents_df["status"].value_counts().to_dict()
                lines.append(f"- Incident status breakdown: {status_counts}")

            if "incident_type" in incidents_df.columns:
                top_types = (
                    incidents_df["incident_type"]
                    .value_counts()
                    .head(5)
                    .to_dict()
                )
                lines.append(f"- Top incident types: {top_types}")

            lines.append("")

    # ---- TICKETS CONTEXT ----
    if tickets_df is not None and isinstance(tickets_df, pd.DataFrame):
        if any(k in q for k in ["ticket", "it ticket", "helpdesk", "priority"]):
            lines.append("TICKETS SUMMARY:")
            lines.append(f"- Total tickets: {len(tickets_df)}")

            if "status" in tickets_df.columns:
                t_status = tickets_df["status"].value_counts().to_dict()
                lines.append(f"- Tickets by status: {t_status}")

            if "priority" in tickets_df.columns:
                t_priority = tickets_df["priority"].value_counts().to_dict()
                lines.append(f"- Tickets by priority: {t_priority}")

            lines.append("")

    # ---- DATASETS CONTEXT ----
    if datasets_df is not None and isinstance(datasets_df, pd.DataFrame):
        if any(k in q for k in ["dataset", "data set", "feeds", "metadata", "source"]):
            lines.append("DATASETS SUMMARY:")
            lines.append(f"- Total datasets: {len(datasets_df)}")

            if "source" in datasets_df.columns:
                ds_source = datasets_df["source"].value_counts().to_dict()
                lines.append(f"- Datasets by source: {ds_source}")

            if "record_count" in datasets_df.columns:
                total_records = int(datasets_df["record_count"].sum())
                lines.append(f"- Total records across all datasets: {total_records}")

            # Optional: show a few names
            if "dataset_name" in datasets_df.columns:
                sample_names = (
                    datasets_df["dataset_name"]
                    .dropna()
                    .astype(str)
                    .head(5)
                    .tolist()
                )
                if sample_names:
                    lines.append(f"- Example dataset names: {sample_names}")

            lines.append("")

    return "\n".join(lines).strip()


# --------------- PROMPT BUILDER -------------- #
def build_prompt_from_history(history, username: str, user_question: str) -> str:
    """
    Combine: persona + light 'memory' of user + portal data context + conversation history.
    """
    # Lightweight "memory" about the user (static + username based)
    user_memory = (
        f"The user's login name is '{username}'. "
        "They are a cybersecurity student who also enjoys music, singing, guitar, "
        "gaming and building side hustles. They care about improving themselves, "
        "learning tech, and becoming financially independent. Respond in a balanced "
        "tone: friendly, slightly casual, but still clear and competent.\n"
    )

    data_context = build_data_context(user_question)

    lines = [
        "System: You are a friendly, balanced and knowledgeable AI assistant. "
        "You talk like a smart friend — relaxed, positive, and supportive — but you "
        "still explain things clearly and accurately. Avoid making up factual details "
        "about their database; only use what is given in the data context.\n",
        "Here is what you know about the user:",
        user_memory,
    ]

    if data_context:
        lines.append("\nHere is the current Cyber Portal data context (aggregated):")
        lines.append(data_context)

    lines.append("\nConversation so far:")

    for msg in history:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        prefix = "Assistant" if role == "assistant" else "User"
        lines.append(f"{prefix}: {content}")

    lines.append("Assistant:")
    return "\n".join(lines)


# --------------- DISPLAY HISTORY ------------- #
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------- TOP BAR: CLEAR + INFO ------- #
c1, c2 = st.columns([1, 1])
with c1:
    if st.button("🧹 Clear Chat"):
        st.session_state.ai_chat = [
            {
                "role": "assistant",
                "content": (
                    "Chat cleared 🧼. Fresh start! "
                    "Ask me anything again, from life advice to SOC data questions 😄"
                ),
            }
        ]
        st.experimental_rerun()

with c2:
    st.info(f"Logged in as **{username}** (`{role}`)")

st.markdown("---")

# --------------- USER INPUT ------------------ #
prompt = st.chat_input("Ask me anything… tech, life, music, business, or your SOC data 😎")

if prompt and not error_msg:

    # Save + show user message
    st.session_state.ai_chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --------------- AI RESPONSE -------------- #
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("_Thinking with max brain cells… 🤓_")

        full_reply = ""
        try:
            convo_prompt = build_prompt_from_history(
                st.session_state.ai_chat,
                username=username,
                user_question=prompt,
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=convo_prompt,
            )

            full_reply = (response.text or "").strip()
            if not full_reply:
                full_reply = (
                    "Weird, I didn't get any text back from Gemini 😅 "
                    "Try asking again in a slightly different way."
                )

        except Exception as e:
            full_reply = f"⚠️ Error while talking to Gemini: `{e}`"

        placeholder.markdown(full_reply)

    # Store assistant reply in history
    st.session_state.ai_chat.append(
        {
            "role": "assistant",
            "content": full_reply,
        }
    )

elif prompt and error_msg:
    st.error("Prompt received, but Gemini is not configured correctly. Check your API key.")
