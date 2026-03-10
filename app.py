import streamlit as st
from storage import list_diagrams, new_diagram

st.set_page_config(
    page_title="Mermaid Studio",
    page_icon="🧜",
    layout="wide"
)

# UI Styling: Hide sidebar and style the grid
st.markdown("""
<style>
    /* Hide the default sidebar and toggle */
    [data-testid="collapsedControl"] { display: none; }
    [data-testid="stSidebar"] { display: none; }
    
    /* Clean up top padding */
    .block-container { padding-top: 3rem; max-width: 1200px; }
    
    /* Style columns to look like modern cards */
    div[data-testid="column"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="column"]:hover {
        border-color: #3b82f6;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([5, 1])
with col1:
    st.title("🧜 Mermaid Studio")
with col2:
    st.write("") # Spacer for vertical alignment
    if st.button("➕ New Diagram", use_container_width=True, type="primary"):
        diagram_id = new_diagram()
        st.session_state.diagram_id = diagram_id
        st.switch_page("pages/editor.py")

st.divider()

diagrams = list_diagrams()

if len(diagrams) == 0:
    st.info("No diagrams yet. Click **New Diagram** to create one.")
    st.stop()

# Grid Layout for Diagrams
cols = st.columns(3, gap="large")

for i, diagram in enumerate(diagrams):
    with cols[i % 3]:
        st.subheader(f"📊 {diagram['title']}")
        st.write("") # Spacing
        if st.button("Open Editor", key=diagram["id"], use_container_width=True):
            st.session_state.diagram_id = diagram["id"]
            st.switch_page("pages/editor.py")