import streamlit as st
import os
from dotenv import load_dotenv

# Import Agents
from agents.planner import PlannerAgent
from agents.retriever import RetrieverAgent
from agents.verifier import VerifierAgent
from agents.synthesizer import SynthesizerAgent
from ingest import ingest_file # Import ingestion logic

load_dotenv()

# Path Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static", "papers")
os.makedirs(STATIC_DIR, exist_ok=True)

st.set_page_config(page_title="Refined Research Assistant", page_icon="🧠", layout="wide")

st.title("🧠 AI Research Assistant")
st.markdown("Ask complex research questions and get evidence-backed answers.")

# Sidebar for configuration/status
with st.sidebar:
    st.header("Upload Research Papers")
    uploaded_files = st.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)
    
    if uploaded_files:
        if st.button(f"Ingest {len(uploaded_files)} file(s)"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            for idx, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing {uploaded_file.name}...")
                save_path = os.path.join(STATIC_DIR, uploaded_file.name)
                
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                success, msg = ingest_file(save_path)
                results.append((uploaded_file.name, success, msg))
                progress_bar.progress((idx + 1) / len(uploaded_files))
            
            status_text.text("Processing complete.")
            
            # Show summary
            for fname, success, msg in results:
                if success:
                    st.success(f"✅ **{fname}**: {msg}")
                else:
                    st.error(f"❌ **{fname}**: {msg}")

# Initialize Session State for Chat History
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Initialize Agents
if 'planner' not in st.session_state:
    st.session_state.planner = PlannerAgent()
if 'retriever' not in st.session_state:
    st.session_state.retriever = RetrieverAgent()
if 'verifier' not in st.session_state:
    st.session_state.verifier = VerifierAgent()
if 'synthesizer' not in st.session_state:
    st.session_state.synthesizer = SynthesizerAgent()

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if query := st.chat_input("Enter your research question:"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(query)
    # Add to history
    st.session_state.messages.append({"role": "user", "content": query})

    # Create a container for the process visualization
    with st.status("🤖 Analyzing Research Papers...", expanded=True) as status:
        st.write("🧠 **Planning Strategy...**")
        sub_queries = st.session_state.planner.plan(query)
        st.write(sub_queries)
        
        st.write("🔍 **Retrieving Evidence...**")
        all_chunks = []
        for sq in sub_queries:
            chunks = st.session_state.retriever.retrieve(sq)
            all_chunks.extend(chunks)
            
        st.write(f"🕵️ **Verifying {len(all_chunks)} raw excerpts...**")
        verified_chunks = st.session_state.verifier.verify(all_chunks)
        st.write(f"✅ Found {len(verified_chunks)} high-quality excerpts.")
        
        st.write("📝 **Synthesizing Answer...**")
        answer = st.session_state.synthesizer.synthesize(query, verified_chunks)
        
        status.update(label="Analysis Complete", state="complete", expanded=False)

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(answer)
    
    # Add to history
    st.session_state.messages.append({"role": "assistant", "content": answer})

