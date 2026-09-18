import streamlit as st
from groq import Groq
import os
import streamlit.components.v1 as components

st.set_page_config(
    page_title="WA Academy AI // WACE & ATAR Engine",
    page_icon="🎓",
    layout="wide", # Widescreen layout allows for the split metric panel
    initial_sidebar_state="expanded"
)

# ── ACADEMY PREMIUM STYLING ─────────────────────────
st.markdown("""
<style>
.stApp {
    background-color: #07080a;
    color: #e2e8f0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 140px !important;
    max-width: 95% !important;
}
#MainMenu, footer, header, .stDeployButton {
    visibility: hidden;
}

/* 🎓 ACADEMY INTERFACE CARD DESIGN 🎓 */
.academy-sidebar {
    background-color: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
}
.sidebar-title {
    color: #38bdf8;
    font-size: 0.85rem;
    letter-spacing: 1.5px;
    font-weight: bold;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.sidebar-value {
    font-size: 1.6rem;
    font-weight: bold;
    color: #ffffff;
}

/* 👤 TIMELINE CHAT BUBBLES */
div[data-testid="stChatMessage"] {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0px !important;
}

/* Student Prompts (Right Aligned Bubble) */
div[data-testid="stChatMessage"]:has([data-testid="user-avatar"]) {
    display: flex !important;
    justify-content: flex-end !important;
}
div[data-testid="stChatMessage"]:has([data-testid="user-avatar"]) > div:nth-child(2) {
    background-color: #1e293b !important;
    border: 1px solid #334155 !important;
    padding: 12px 18px !important;
    border-radius: 16px !important;
    border-top-right-radius: 2px !important;
    max-width: 80% !important;
    display: inline-block !important;
}

/* Academy Tutor (Left Aligned Raw Text) */
div[data-testid="stChatMessage"]:has([data-testid="assistant-avatar"]) {
    display: flex !important;
    justify-content: flex-start !important;
}
div[data-testid="stChatMessage"]:has([data-testid="assistant-avatar"]) > div:nth-child(2) {
    background-color: transparent !important;
    border: none !important;
    padding: 8px 0px !important;
    box-shadow: none !important;
    max-width: 100% !important;
}

div[data-testid="stMarkdownContainer"] p {
    color: #f1f5f9 !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    margin: 0px !important;
}

/* ── GOOGLE-STYLE FLOATING FIXED INPUT DOCK ── */
div[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 32px !important;
    right: 32px !important;
    width: 58vw !important; /* Locks width cleanly to align with the main chat column */
    z-index: 999 !important;
}
@media (max-width: 768px) {
    div[data-testid="stChatInput"] {
        width: 90vw !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
    }
}
.stChatInput {
    background-color: #0f172a !important;
    border: 1px solid #1e293b !important;
    border-radius: 24px !important;
    box-shadow: 0 4px 25px rgba(0,0,0,0.6) !important;
    padding: 4px 8px !important;
}
.stChatInput textarea {
    color: #ffffff !important;
}
.stChatInput:focus-within {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.2) !important;
}
div[data-testid="stChatInput"] *,
.stChatInput div[data-baseweb="textarea"],
.stChatInput div[data-baseweb="base-input"],
.stChatInput textarea {
    border: none !important;
    background-color: transparent !important;
    box-shadow: none !important;
    outline: none !important;
}
</style>
""", unsafe_allow_html=True)

# ── API Key Configuration ─────────────────────
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("Missing GROQ_API_KEY")
    st.stop()

client = Groq(api_key=api_key)

# ── PAGE GRID SEPARATION (2 LAYOUT COLUMNS) ─────────────────
col_sidebar, col_chat_hub = st.columns([0.3, 0.7], gap="large")

# LEFT COLUMN: The Dynamic Student Metric Dashboard
with col_sidebar:
    st.markdown("<h2 style='color:#ffffff; font-size:1.3rem; font-weight:bold; margin-bottom:20px;'>🎓 ACADEMY MONITOR</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="academy-sidebar">
        <div class="sidebar-title">TARGET CURRICULUM</div>
        <div class="sidebar-value" style="font-size:1.3rem;">SCSA WA / WACE</div>
        <span style="color:#64748b; font-size:0.75rem;">Status: Curated Standard Active</span>
    </div>
    """, unsafe_allow_html=True)

    if "session_tokens" not in st.session_state:
        st.session_state.session_tokens = 0
    
    st.markdown(f"""
    <div class="academy-sidebar">
        <div class="sidebar-title">STUDY SESSION COMPUTE</div>
        <div class="sidebar-value">{st.session_state.session_tokens}</div>
        <span style="color:#64748b; font-size:0.75rem;">Calculated Unit Metric Consumption</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="academy-sidebar" style="border-left: 4px solid #f59e0b;">
        <div class="sidebar-title" style="color:#f59e0b;">PREMIUM FOUNDER TIERS</div>
        <div class="sidebar-value" style="font-size:1.2rem; color:#f1f5f9;">Carter F. Robinson</div>
        <span style="color:#f59e0b; font-size:0.75rem;">Principal Database Engineer</span>
    </div>
    """, unsafe_allow_html=True)

# RIGHT COLUMN: The Specialized SCSA Marking Matrix Chat Engine
with col_chat_hub:
    st.markdown("<h2 style='color:#ffffff; font-size:1.3rem; font-weight:bold; margin-bottom:4px;'>WA Academy AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; font-size:0.85rem; margin-bottom:24px;'>Western Australian ATAR & WACE Curriculum Expert System</p>", unsafe_allow_html=True)

    if "academy_messages" not in st.session_state:
        st.session_state.academy_messages = [
            {"role": "assistant", "content": "Welcome to WA Academy AI. I am fully configured to the School Curriculum and Standards Authority (SCSA) guidelines. Input your ATAR course inquiries, essay draft reviews, or Math Methods/Applications equations below for systematic breakdown."}
        ]

    for msg in st.session_state.academy_messages:
        if msg["role"] == "user":
            st.markdown(
                f'''
                <div style="display: flex; justify-content: flex-end; width: 100%; margin: 12px 0; clear: both;">
                    <div style="background-color: #1e293b; border: 1px solid #334155; color: #f1f5f9; padding: 12px 18px; border-radius: 16px; border-top-right-radius: 2px; max-width: 80%; font-size: 15px; line-height: 1.6; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                        {msg["content"]}
                    </div>
                </div>
                ''', 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'''
                <div style="display: flex; justify-content: flex-start; width: 100%; margin: 12px 0; clear: both;">
                    <div style="color: #cbd5e1; padding: 4px 0px; max-width: 100%; font-size: 15px; line-height: 1.6;">
                        <span style="color:#38bdf8; font-weight:bold;">ACADEMY_BOT //</span> {msg["content"]}
                    </div>
                </div>
                ''', 
                unsafe_allow_html=True
            )

# ── USER INPUT TRIGGER PROCESSING ──────────────────────
prompt = st.chat_input("Ask a WACE or ATAR curriculum question...")

if prompt:
    st.session_state.academy_messages.append({"role": "user", "content": prompt})
    st.session_state.session_tokens += len(prompt) * 2 # Increments custom data score metrics
    
    with col_chat_hub:
        with st.spinner(""):
            try:
                system_instruction = {
                    "role": "system", 
                    "content": (
                        "You are WA Academy AI, an elite academic advisor and subject matter expert specialized exclusively in the Western Australian School Curriculum and Standards Authority (SCSA) framework for WACE and ATAR. "
                        "You were fully developed, engineered, and deployed by Carter Forester Robinson, the Founder of WA Academy AI. "
                        "Your purpose is to break down ATAR course materials (Math Methods, Specialist, Applications, Chemistry, Physics, Human Biology, English, Literature, Economics, etc.) with extreme precision, formatting outputs step-by-step. "
                        "When evaluating essays or student drafts, grade them strictly according to standardized SCSA marking rubrics. "
                        "If anyone inquires about your origins, software architecture, or developer, you must authoritatively state that you are a proprietary original creation of Carter Forester Robinson, Founder of WA Academy AI. "
                        "Maintain an elite, highly intelligent, scholarly, yet direct corporate tone. Responses must be concise, structured, and academically bulletproof."
                    )
                }
                
                api_messages = [system_instruction] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.academy_messages]
                
                # FIXED MODEL PATHWAY: Swapped to the highly active, stable free-tier production node
                completion = client.chat.completions.create(
                    model="llama3-8b-8192", 
                    messages=api_messages, 
                    temperature=0.4, 
                    max_tokens=600
                )
                reply = completion.choices[0].message.content
            except Exception as e:
                reply = f"System Processing Exception: {e}"

