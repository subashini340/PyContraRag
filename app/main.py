import streamlit as st
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.components.styles import apply_custom_css
from src.agent import PyContraAgent

# 1. Page Config
st.set_page_config(page_title="PyContraRAG", page_icon="🐍", layout="wide", initial_sidebar_state="expanded")

# 2. Sidebar (With Theme Toggle Option)
with st.sidebar:
    st.markdown("## 🐍 PyContraRAG")
    st.markdown("---")
    
    # Theme Toggle Option
    st.markdown("### ⚙️ Preferences")
    theme_choice = st.toggle("Dark Mode", value=True)
    theme_str = "dark" if theme_choice else "light"
    
    # Apply the theme dynamically based on toggle
    apply_custom_css(theme=theme_str)

    st.markdown("---")
    st.markdown("### 📊 System Status")
    st.success("ChromaDB: Connected")
    st.success("NLI Engine: Online")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 3. Main Area - Hero Section
st.markdown("<h1>🐍 PyContraRAG</h1>", unsafe_allow_html=True)
st.markdown("<div class='app-caption'>Detect contradictions. Score credibility. Get the absolute truth.</div>", unsafe_allow_html=True)

# 4. Load Agent
@st.cache_resource
def load_agent():
    return PyContraAgent()
agent = load_agent()

# 5. Chat History State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input
if prompt := st.chat_input("Ask a Python question (e.g., Does dictionary maintain insertion order?)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing documents..."):
            try:
                # Format history
                history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])
                
                response_data = agent.process_query(prompt, chat_history=history_str)
                final_answer = response_data["answer"]
                details = response_data["details"]

                # Display Answer
                st.markdown(final_answer)
                st.markdown("<br>", unsafe_allow_html=True)

                # Zomato-style Source Cards
                if details:
                    st.markdown("### 📚 Source Analysis")
                    col1, col2 = st.columns(2)
                    s1, s2 = details['source_1'], details['source_2']
                    
                    with col1:
                        badge_class_1 = "badge-high" if s1['score'] > 0.7 else "badge-low"
                        st.markdown(f"""
                        <div class="z-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <h4 style="margin: 0;">Python v{s1['version']}</h4>
                                <span class="{badge_class_1}">Trust: {s1['score']*100:.0f}%</span>
                            </div>
                            <p style="font-size: 0.9rem; color: #888; margin-top: 15px; line-height: 1.5;">
                                "{s1['text'][:150]}..."
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        with st.expander("Read Full Document"):
                            st.write(s1['text'])
                            
                    with col2:
                        badge_class_2 = "badge-high" if s2['score'] > 0.7 else "badge-low"
                        st.markdown(f"""
                        <div class="z-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <h4 style="margin: 0;">Python v{s2['version']}</h4>
                                <span class="{badge_class_2}">Trust: {s2['score']*100:.0f}%</span>
                            </div>
                            <p style="font-size: 0.9rem; color: #888; margin-top: 15px; line-height: 1.5;">
                                "{s2['text'][:150]}..."
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        with st.expander("Read Full Document"):
                            st.write(s2['text'])

                    if details['conflict']['is_conflict']:
                        st.info("💡 Note: Contradiction detected between versions. The newer version was prioritized based on higher credibility.")

                st.session_state.messages.append({"role": "assistant", "content": final_answer})
                
            except Exception as e:
                st.error(f"Error: {str(e)}")