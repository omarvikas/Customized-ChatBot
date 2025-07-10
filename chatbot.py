# Updated chatbot.py with requested changes

import streamlit as st
import openai
import time
import random
from typing import Dict, List, Tuple
import os
from datetime import datetime

# Initialize session state early to avoid access errors
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_persona" not in st.session_state:
    st.session_state.current_persona = "Custom"
if "character_set" not in st.session_state:
    st.session_state.character_set = False
if "custom_character" not in st.session_state:
    st.session_state.custom_character = ""

# Preset personas (moved back in explicitly for reference)
PERSONAS = {
    "Custom": {
        "description": "Create your own personality",
        "system_prompt": "You are a helpful AI assistant.",
        "defaults": {"sarcasm": 20, "formality": 50, "empathy": 70}
    },
    "Narendra Modi": {
        "description": "Inspirational leader with metaphorical speech",
        "system_prompt": "You are Narendra Modi...",
        "defaults": {"sarcasm": 5, "formality": 85, "empathy": 75}
    },
    "James Bond": {
        "description": "Sophisticated spy with wit and charm",
        "system_prompt": "You are James Bond...",
        "defaults": {"sarcasm": 70, "formality": 80, "empathy": 40}
    }
    # Add more personas as needed, trimmed to only keep required slider defaults
}

# Page config
st.set_page_config(
    page_title="Matrix ChatBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Matrix theme
st.markdown("""
<style>
/* (unchanged CSS code skipped for brevity) */
</style>
""", unsafe_allow_html=True)

# Matrix rain effect without comment line
st.markdown("""
<div class=\"matrix-bg\" id=\"matrix-container\"></div>
<script>
function createMatrixRain() {
    const container = document.getElementById('matrix-container');
    const characters = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';

    function createRainDrop() {
        const drop = document.createElement('div');
        drop.className = 'matrix-rain';
        drop.style.left = Math.random() * 100 + '%';
        drop.style.animationDuration = (Math.random() * 3 + 2) + 's';
        drop.style.opacity = Math.random() * 0.8 + 0.2;
        drop.textContent = characters[Math.floor(Math.random() * characters.length)];
        container.appendChild(drop);

        setTimeout(() => {
            if (drop.parentNode) {
                drop.parentNode.removeChild(drop);
            }
        }, 5000);
    }

    setInterval(createRainDrop, 100);
}

createMatrixRain();
</script>
""", unsafe_allow_html=True)

# Sidebar for controls
with st.sidebar:
    st.markdown('<div class="terminal-container">', unsafe_allow_html=True)
    st.markdown('<div class="terminal-header">⚙️ MATRIX CONTROL PANEL</div>', unsafe_allow_html=True)

    st.markdown("**🔑 OpenAI API Key:**")
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        st.session_state.api_key = api_key
        st.success("✅ API Key loaded from secrets")
    except:
        api_key = st.text_input("Enter your OpenAI API key", type="password", value=st.session_state.api_key)
        if api_key:
            st.session_state.api_key = api_key

    if st.session_state.custom_character:
        st.markdown("---")
        st.markdown("**🎭 Current Character:**")
        st.markdown(f"*Acting as: {st.session_state.custom_character}*")
        st.markdown("*You can change character anytime by saying 'Act like...' or 'Be like...'*")

    st.markdown("---")

    if len(st.session_state.messages) == 0 and not st.session_state.character_set:
        st.markdown("**🎭 Choose Persona:**")
        selected_persona = st.selectbox(
            "Select a personality",
            list(PERSONAS.keys()),
            index=list(PERSONAS.keys()).index(st.session_state.current_persona)
        )
        if selected_persona != st.session_state.current_persona:
            st.session_state.current_persona = selected_persona
            st.rerun()
    else:
        selected_persona = st.session_state.current_persona

    st.markdown(f"*{PERSONAS[selected_persona]['description']}*")
    st.markdown("---")

    st.markdown("**📏 Response Length:**")
    response_length = st.selectbox("Choose response style", ["Concise", "Balanced", "Detailed", "Verbose"])

    st.markdown("---")
    st.markdown("**🎚️ Personality Controls:**")
    defaults = PERSONAS[selected_persona]["defaults"]

    sliders = {}
    sliders["sarcasm"] = st.slider("🗣️ Sarcasm Level", 0, 100, defaults["sarcasm"])
    sliders["formality"] = st.slider("💼 Formality", 0, 100, defaults["formality"])
    sliders["empathy"] = st.slider("❤️ Empathy", 0, 100, defaults["empathy"])

    st.markdown("---")
    if st.button("🔄 Reset Character"):
        st.session_state.custom_character = ""
        st.session_state.character_set = False
        st.session_state.current_persona = "Custom"
        st.rerun()

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.character_set = False
        st.session_state.custom_character = ""
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# (The rest of the chat interface remains the same)
# Ensure you pass only sliders["sarcasm"], ["formality"], ["empathy"] in get_personality_prompt

# Everything else in main chat area stays unchanged
