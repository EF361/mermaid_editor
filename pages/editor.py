# pages/editor.py (FULL FILE)
import streamlit as st
from streamlit_ace import st_ace

from storage import load_diagram, save_diagram
from components import mermaid

# Page config for this page (optional: ensure wide)
st.set_page_config(layout="wide")

# small style tweaks for spacing
st.markdown("""
    <style>
      .block-container { padding-top: 1rem; }
      .stTextInput > label { font-weight: 600; color: #111827; }
      .title-row { display:flex; gap:12px; align-items:center; margin-bottom:8px; }
      .back-btn { margin-left: 12px; }
    </style>
""", unsafe_allow_html=True)

diagram_id = st.session_state.get("diagram_id")
if not diagram_id:
    st.error("No diagram selected")
    st.stop()

diagram = load_diagram(diagram_id)

# Top row: title + back button
col_title, col_back = st.columns([9,1])
with col_title:
    title = st.text_input("Diagram Title", value=diagram.get("title", "Untitled Diagram"))
with col_back:
    if st.button("← Back"):
        st.switch_page("app.py")

# Choose column ratio: left editor narrower, right preview larger
editor_col, preview_col = st.columns([0.9, 1.3], gap="large")

# editor height and preview height in px
editor_height = 620
preview_height = 740

with editor_col:
    st.markdown("#### Code")
    code = st_ace(
        value=diagram.get("code", ""),
        language="markdown",
        theme="monokai",
        height=editor_height,
        auto_update=True,
        key=f"ace_{diagram_id}"
    )

with preview_col:
    st.markdown("#### Preview")
    # pass title and explicit height so the component sizes predictably
    mermaid(code if code is not None else "", title if title else "diagram", height=preview_height)

# Save on every change (simple auto-save)
save_diagram(diagram_id, title, code)