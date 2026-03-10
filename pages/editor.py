# pages/editor.py
import streamlit as st
from streamlit_ace import st_ace
from storage import load_diagram, save_diagram
from components import mermaid

st.set_page_config(page_title="Editor", page_icon="🧜", layout="wide")

# UI Styling for the Editor
st.markdown("""
<style>
    /* Hide the default sidebar */
    [data-testid="collapsedControl"] { display: none; }
    [data-testid="stSidebar"] { display: none; }
    
    /* Push everything down so nothing hits the top ceiling */
    .block-container { padding-top: 4rem !important; }
    
    /* Make the parent invisible box taller so it doesn't cut off the bottom of the text */
    div[data-baseweb="input"] {
        background-color: transparent !important;
        border: none !important;
        min-height: 60px !important; 
    }
    div[data-baseweb="input"] > div {
        background-color: transparent !important;
        border: none !important;
        min-height: 60px !important;
    }
    
    /* Gently push the text input container down */
    [data-testid="stTextInput"] {
        margin-top: 5px;
    }

    /* Style the title text so it fits perfectly */
    input[aria-label="Diagram Title"] {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #111827 !important;
        padding: 0px 10px !important;
        height: 60px !important; 
        line-height: normal !important; /* Let the browser handle spacing naturally */
    }
    input[aria-label="Diagram Title"]:focus {
        border-bottom: 2px solid #3b82f6 !important;
        border-radius: 0px !important;
    }
    
    /* Push the back button down to align exactly with the title */
    [data-testid="stButton"] {
        margin-top: 15px; 
    }
    
    /* Style for the Code and Preview labels */
    .section-label {
        font-size: 13px;
        font-weight: 700;
        color: #6b7280;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

diagram_id = st.session_state.get("diagram_id")
if not diagram_id:
    st.error("No diagram selected")
    st.stop()

diagram = load_diagram(diagram_id)

# Top row: Back Button + Seamless Title
col_back, col_title = st.columns([1, 11], gap="medium")
with col_back:
    if st.button("← Back", use_container_width=True):
        st.switch_page("app.py")
with col_title:
    title = st.text_input("Diagram Title", value=diagram.get("title", "Untitled Diagram"), label_visibility="collapsed")

st.write("") # Vertical pacing

# Editor & Preview Layout
editor_col, preview_col = st.columns([1, 1.2], gap="large")

editor_height = 700

with editor_col:
    st.markdown('<div class="section-label">💻 MERMAID CODE</div>', unsafe_allow_html=True)
    code = st_ace(
        value=diagram.get("code", ""),
        language="markdown",
        theme="tomorrow_night", 
        height=editor_height,
        auto_update=True,
        key=f"ace_{diagram_id}",
        font_size=14,
        show_gutter=True,
    )

with preview_col:
    st.markdown('<div class="section-label">👁️ PREVIEW</div>', unsafe_allow_html=True)
    mermaid(code if code is not None else "", title if title else "diagram", height=editor_height)

# Auto-save
save_diagram(diagram_id, title, code)