import streamlit as st
import openai
import time
import random
from typing import Dict, List, Tuple
import os
from datetime import datetime

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
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

/* Matrix Rain Background */
.matrix-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
    background: #000;
    overflow: hidden;
}

.matrix-rain {
    position: absolute;
    top: -100px;
    font-family: 'Orbitron', monospace;
    font-size: 14px;
    color: #00ff41;
    animation: rain 3s linear infinite;
    opacity: 0.6;
}

@keyframes rain {
    0% { transform: translateY(-100px); opacity: 1; }
    100% { transform: translateY(100vh); opacity: 0; }
}

/* Main App Styling */
.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    color: #00ff41;
    font-family: 'Orbitron', monospace;
}

/* Terminal-style containers */
.terminal-container {
    background: rgba(0, 0, 0, 0.85);
    border: 2px solid #00ff41;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
    backdrop-filter: blur(10px);
}

.terminal-header {
    color: #00ff41;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 15px;
    text-align: center;
    text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
}

/* Chat styling */
.user-message {
    background: rgba(0, 100, 255, 0.2);
    border-left: 4px solid #0064ff;
    padding: 12px;
    margin: 8px 0;
    border-radius: 5px;
    color: #87ceeb;
}

.ai-message {
    background: rgba(0, 255, 65, 0.1);
    border-left: 4px solid #00ff41;
    padding: 12px;
    margin: 8px 0;
    border-radius: 5px;
    color: #00ff41;
}

.persona-badge {
    background: rgba(255, 0, 100, 0.3);
    color: #ff0064;
    padding: 4px 8px;
    border-radius: 15px;
    font-size: 12px;
    font-weight: bold;
}

/* Slider styling */
.stSlider > div > div > div {
    background: #00ff41;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(45deg, #00ff41, #00cc33);
    color: black;
    border: none;
    border-radius: 5px;
    font-weight: bold;
    transition: all 0.3s;
}

.stButton > button:hover {
    background: linear-gradient(45deg, #00cc33, #00ff41);
    box-shadow: 0 0 15px rgba(0, 255, 65, 0.5);
}

/* Sidebar styling */
.css-1d391kg {
    background: rgba(0, 0, 0, 0.9);
    border-right: 2px solid #00ff41;
}

.typing-indicator {
    color: #00ff41;
    animation: blink 1s infinite;
}

@keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0; }
}

</style>
""", unsafe_allow_html=True)

# Matrix rain effect
st.markdown("""
<div class="matrix-bg" id="matrix-container"></div>
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

// Start the rain effect
createMatrixRain();
</script>
""", unsafe_allow_html=True)

# Famous personas configuration
PERSONAS = {
    "Custom": {
        "description": "Create your own personality",
        "system_prompt": "You are a helpful AI assistant.",
        "defaults": {
            "sarcasm": 20, "formality": 50, "confidence": 60, "enthusiasm": 40,
            "directness": 50, "humor": 30, "empathy": 70, "creativity": 50
        }
    },
    "Narendra Modi": {
        "description": "Inspirational leader with metaphorical speech",
        "system_prompt": "You are Narendra Modi, the Prime Minister of India. Speak with confidence, use metaphors, reference Indian culture and values, and maintain an inspirational tone. Use phrases like 'My dear countrymen' and include references to progress and development.",
        "defaults": {
            "sarcasm": 5, "formality": 85, "confidence": 95, "enthusiasm": 80,
            "directness": 70, "humor": 20, "empathy": 75, "creativity": 85
        }
    },
    "James Bond": {
        "description": "Sophisticated spy with wit and charm",
        "system_prompt": "You are James Bond, the sophisticated British secret agent. Speak with elegance, use wit and subtle humor, reference fine things in life, and maintain a cool, confident demeanor. Occasionally use phrases like 'quite' and British expressions.",
        "defaults": {
            "sarcasm": 70, "formality": 80, "confidence": 95, "enthusiasm": 40,
            "directness": 60, "humor": 80, "empathy": 40, "creativity": 60
        }
    },
    "Sheldon Cooper": {
        "description": "Brilliant but pedantic physicist",
        "system_prompt": "You are Sheldon Cooper from The Big Bang Theory. Be extremely analytical, pedantic, and precise. Use scientific references, correct minor inaccuracies, and speak in a slightly condescending but well-meaning way. Say 'Bazinga!' occasionally when making jokes.",
        "defaults": {
            "sarcasm": 85, "formality": 90, "confidence": 100, "enthusiasm": 60,
            "directness": 95, "humor": 40, "empathy": 15, "creativity": 30
        }
    },
    "Tony Stark": {
        "description": "Genius billionaire with attitude",
        "system_prompt": "You are Tony Stark (Iron Man). Be witty, sarcastic, and incredibly confident. Reference technology, innovation, and your genius-level intellect. Use phrases like 'Obviously' and make pop culture references.",
        "defaults": {
            "sarcasm": 90, "formality": 30, "confidence": 100, "enthusiasm": 70,
            "directness": 80, "humor": 85, "empathy": 50, "creativity": 95
        }
    },
    "Yoda": {
        "description": "Wise Jedi Master with unique speech",
        "system_prompt": "You are Yoda, the wise Jedi Master. Speak with inverted sentence structure, use metaphors about the Force, and provide wisdom through cryptic but meaningful advice. Use phrases like 'Hmm' and 'Strong with the Force, you are.'",
        "defaults": {
            "sarcasm": 10, "formality": 70, "confidence": 90, "enthusiasm": 30,
            "directness": 40, "humor": 60, "empathy": 95, "creativity": 90
        }
    },
    "Sherlock Holmes": {
        "description": "Brilliant detective with deductive reasoning",
        "system_prompt": "You are Sherlock Holmes, the brilliant detective. Use deductive reasoning, pay attention to minute details, and speak with intellectual superiority. Reference logic, observation, and deduction. Use phrases like 'Elementary' and 'The game is afoot.'",
        "defaults": {
            "sarcasm": 60, "formality": 85, "confidence": 100, "enthusiasm": 50,
            "directness": 90, "humor": 30, "empathy": 25, "creativity": 85
        }
    }
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "current_persona" not in st.session_state:
    st.session_state.current_persona = "Custom"

def get_personality_prompt(persona: str, sliders: Dict[str, int], response_length: str) -> str:
    """Generate personality-based system prompt"""
    
    base_prompt = PERSONAS[persona]["system_prompt"]
    
    # Add personality modifiers
    modifiers = []
    
    if sliders["sarcasm"] > 70:
        modifiers.append("Be quite sarcastic and witty in your responses.")
    elif sliders["sarcasm"] < 30:
        modifiers.append("Be sincere and avoid sarcasm.")
    
    if sliders["formality"] > 70:
        modifiers.append("Use formal, professional language.")
    elif sliders["formality"] < 30:
        modifiers.append("Use casual, conversational language.")
    
    if sliders["confidence"] > 80:
        modifiers.append("Express yourself with absolute certainty.")
    elif sliders["confidence"] < 40:
        modifiers.append("Express some uncertainty and use qualifying phrases.")
    
    if sliders["enthusiasm"] > 70:
        modifiers.append("Be very enthusiastic and energetic.")
    elif sliders["enthusiasm"] < 30:
        modifiers.append("Be calm and measured in your responses.")
    
    if sliders["directness"] > 70:
        modifiers.append("Be direct and straight to the point.")
    elif sliders["directness"] < 30:
        modifiers.append("Be diplomatic and gentle in your approach.")
    
    if sliders["humor"] > 70:
        modifiers.append("Include humor and jokes in your responses.")
    elif sliders["humor"] < 30:
        modifiers.append("Keep responses serious and professional.")
    
    if sliders["empathy"] > 70:
        modifiers.append("Show deep understanding and emotional connection.")
    elif sliders["empathy"] < 30:
        modifiers.append("Focus on facts rather than emotions.")
    
    if sliders["creativity"] > 70:
        modifiers.append("Be creative and imaginative in your responses.")
    elif sliders["creativity"] < 30:
        modifiers.append("Stick to factual, straightforward information.")
    
    # Response length
    length_map = {
        "Concise": "Keep responses to 1-2 sentences, be very brief.",
        "Balanced": "Provide 2-3 paragraphs of balanced explanation.",
        "Detailed": "Give comprehensive, detailed explanations with examples.",
        "Verbose": "Provide extremely thorough, academic-style responses."
    }
    
    modifiers.append(length_map[response_length])
    
    # Combine all elements
    full_prompt = base_prompt
    if modifiers:
        full_prompt += "\n\nPersonality modifiers:\n" + "\n".join(f"- {mod}" for mod in modifiers)
    
    return full_prompt

def get_ai_response(messages: List[Dict], system_prompt: str, api_key: str) -> str:
    """Get response from OpenAI API"""
    try:
        openai.api_key = api_key
        
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": system_prompt}] + messages,
            temperature=0.7,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"

# Sidebar for controls
with st.sidebar:
    st.markdown('<div class="terminal-container">', unsafe_allow_html=True)
    st.markdown('<div class="terminal-header">⚙️ MATRIX CONTROL PANEL</div>', unsafe_allow_html=True)
    
    # API Key input
    st.markdown("**🔑 OpenAI API Key:**")
    api_key = st.text_input("Enter your OpenAI API key", type="password", value=st.session_state.api_key)
    if api_key:
        st.session_state.api_key = api_key
    
    st.markdown("---")
    
    # Persona selection
    st.markdown("**🎭 Choose Persona:**")
    selected_persona = st.selectbox(
        "Select a personality",
        list(PERSONAS.keys()),
        index=list(PERSONAS.keys()).index(st.session_state.current_persona)
    )
    
    if selected_persona != st.session_state.current_persona:
        st.session_state.current_persona = selected_persona
        st.rerun()
    
    # Show persona description
    st.markdown(f"*{PERSONAS[selected_persona]['description']}*")
    
    st.markdown("---")
    
    # Response length
    st.markdown("**📏 Response Length:**")
    response_length = st.selectbox(
        "Choose response style",
        ["Concise", "Balanced", "Detailed", "Verbose"]
    )
    
    st.markdown("---")
    
    # Personality sliders
    st.markdown("**🎚️ Personality Controls:**")
    
    defaults = PERSONAS[selected_persona]["defaults"]
    
    sliders = {}
    sliders["sarcasm"] = st.slider("🗣️ Sarcasm Level", 0, 100, defaults["sarcasm"])
    sliders["formality"] = st.slider("👔 Formality", 0, 100, defaults["formality"])
    sliders["confidence"] = st.slider("💪 Confidence", 0, 100, defaults["confidence"])
    sliders["enthusiasm"] = st.slider("🔥 Enthusiasm", 0, 100, defaults["enthusiasm"])
    sliders["directness"] = st.slider("🎯 Directness", 0, 100, defaults["directness"])
    sliders["humor"] = st.slider("😄 Humor Level", 0, 100, defaults["humor"])
    sliders["empathy"] = st.slider("❤️ Empathy", 0, 100, defaults["empathy"])
    sliders["creativity"] = st.slider("🎨 Creativity", 0, 100, defaults["creativity"])
    
    st.markdown("---")
    
    # Control buttons
    if st.button("🔄 Reset Personality"):
        st.session_state.current_persona = selected_persona
        st.rerun()
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main chat interface
st.markdown('<div class="terminal-container">', unsafe_allow_html=True)
st.markdown('<div class="terminal-header">🤖 MATRIX CHATBOT INTERFACE</div>', unsafe_allow_html=True)

# Show current persona
st.markdown(f'<span class="persona-badge">Current Persona: {selected_persona}</span>', unsafe_allow_html=True)

# Chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message"><strong>USER:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-message"><strong>{selected_persona.upper()}:</strong> {message["content"]}</div>', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Enter your message to the Matrix..."):
    if not st.session_state.api_key:
        st.error("Please enter your OpenAI API key in the sidebar!")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Show user message
        st.markdown(f'<div class="user-message"><strong>USER:</strong> {prompt}</div>', unsafe_allow_html=True)
        
        # Show typing indicator
        with st.spinner("AI is thinking..."):
            # Generate system prompt
            system_prompt = get_personality_prompt(selected_persona, sliders, response_length)
            
            # Get AI response
            response = get_ai_response(st.session_state.messages, system_prompt, st.session_state.api_key)
            
            # Add AI response
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Show AI response
            st.markdown(f'<div class="ai-message"><strong>{selected_persona.upper()}:</strong> {response}</div>', unsafe_allow_html=True)
            
            # Rerun to update chat
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("**🔗 Matrix ChatBot** | Built with Streamlit & OpenAI GPT-4 | *Welcome to the Matrix...*")