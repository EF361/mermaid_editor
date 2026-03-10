import streamlit as st
from storage import list_diagrams, new_diagram

st.set_page_config(
    page_title="Mermaid Studio",
    page_icon="🧜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

.block-container{
    padding-top:1.5rem;
}

.card{
    padding:20px;
    border-radius:12px;
    border:1px solid #e5e7eb;
    background:white;
    transition:0.2s;
}

.card:hover{
    border:1px solid #cbd5f5;
    box-shadow:0 6px 18px rgba(0,0,0,0.06);
}

.card-title{
    font-size:18px;
    font-weight:600;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

st.title("Mermaid Studio")

top1, top2 = st.columns([8,1])

with top2:
    if st.button("➕ New"):
        diagram_id = new_diagram()
        st.session_state.diagram_id = diagram_id
        st.switch_page("pages/editor.py")

st.divider()

diagrams = list_diagrams()

if len(diagrams) == 0:
    st.info("No diagrams yet. Click **New** to create one.")
    st.stop()

cols = st.columns(3)

for i, diagram in enumerate(diagrams):

    with cols[i % 3]:

        st.markdown(f"""
        <div class="card">
        <div class="card-title">📊 {diagram["title"]}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open", key=diagram["id"]):
            st.session_state.diagram_id = diagram["id"]
            st.switch_page("pages/editor.py")