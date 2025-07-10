import streamlit as st
import openai
import time
import random
from typing import Dict, List, Tuple
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Multi-Personality Chat Arena",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for vibrant personality themes
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

/* Animated Background */
.main-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
    background: linear-gradient(45deg, #1e3c72, #2a5298, #1e3c72, #2a5298);
    background-size: 400% 400%;
    animation: gradientShift 8s ease infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Floating particles */
.particle {
    position: absolute;
    width: 4px;
    height: 4px;
    background: rgba(255, 255, 255, 0.7);
    border-radius: 50%;
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.7; }
    50% { transform: translateY(-20px) rotate(180deg); opacity: 1; }
}

/* Main App Styling */
.stApp {
    background: transparent;
    color: #ffffff;
    font-family: 'Poppins', sans-serif;
}

/* Vibrant containers */
.chat-arena {
    background: linear-gradient(135deg, rgba(30, 60, 114, 0.9), rgba(42, 82, 152, 0.9));
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 25px;
    margin: 15px 0;
    box-shadow: 0 0 30px rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(15px);
    position: relative;
    overflow: hidden;
}

.chat-arena::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.05), transparent);
    animation: shine 3s ease-in-out infinite;
}

@keyframes shine {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.arena-header {
    color: #ffffff;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    text-align: center;
    text-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
    background-size: 400% 400%;
    animation: textGradient 4s ease infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

@keyframes textGradient {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* Personality-themed chat styling */
.user-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: 2px solid rgba(255, 255, 255, 0.3);
    padding: 15px;
    margin: 10px 0;
    border-radius: 15px;
    color: #ffffff;
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    position: relative;
    overflow: hidden;
}

.user-message::before {
    content: '👤';
    position: absolute;
    top: 10px;
    right: 15px;
    font-size: 20px;
}

/* AI message styles for each persona */
.ai-message-custom {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: 2px solid #667eea;
    color: #ffffff;
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.ai-message-modi {
    background: linear-gradient(135deg, #ff9933 0%, #138808 50%, #0064ff 100%);
    border: 2px solid #ff9933;
    color: #ffffff;
    box-shadow: 0 8px 20px rgba(255, 153, 51, 0.4);
}

.ai-message-bond {
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 50%, #ecf0f1 100%);
    border: 2px solid #ecf0f1;
    color: #ffffff;
    box-shadow: 0 8px 20px rgba(236, 240, 241, 0.3);
}

.ai-message-sheldon {
    background: linear-gradient(135deg, #3498db 0%, #2980b9 50%, #ecf0f1 100%);
    border: 2px solid #3498db;
    color: #ffffff;
    box-shadow: 0 8px 20px rgba(52, 152, 219, 0.4);
}

.ai-message-stark {
    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 50%, #f1c40f 100%);
    border: 2px solid #e74c3c;
    color: #ffffff;
    box-shadow: 0 8px 20px rgba(231, 76, 60, 0.4);
}

.ai-message-yoda {
    background: linear-gradient(135deg, #27ae60 0%, #2ecc71 50%, #16a085 100%);
    border: 2px solid #27ae60;
    color: #ffffff;
    box-shadow: 0 8px 20px rgba(39, 174, 96, 0.4);
}

.ai-message-holmes {
    background: linear-gradient(135deg, #8b4513 0%, #a0522d 50%, #d2691e 100%);
    border: 2px solid #8b4513;
    color: #ffffff;
    box-shadow: 0 8px 20px rgba(139, 69, 19, 0.4);
}

.ai-message {
    padding: 15px;
    margin: 10px 0;
    border-radius: 15px;
    position: relative;
    overflow: hidden;
}

.ai-message::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    animation: messageShine 4s ease-in-out infinite;
}

@keyframes messageShine {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.persona-selector {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    backdrop-filter: blur(10px);
}

.persona-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    padding: 10px;
    margin: 5px 0;
    transition: all 0.3s ease;
    cursor: pointer;
}

.persona-card:hover {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(255, 255, 255, 0.1);
}

.persona-card.selected {
    background: linear-gradient(135deg, #4ecdc4, #44a08d);
    border-color: #4ecdc4;
    color: #ffffff;
}

.thinking-indicator {
    background: linear-gradient(135deg, #ff6b6b, #ee5a52);
    color: white;
    padding: 8px 15px;
    border-radius: 20px;
    font-size: 12px;
    animation: pulse 2s infinite;
    display: inline-block;
    margin: 5px 0;
}

@keyframes pulse {
    0% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(1.05); }
    100% { opacity: 1; transform: scale(1); }
}

/* Sidebar styling */
.sidebar {
    background: linear-gradient(135deg, rgba(30, 60, 114, 0.95), rgba(42, 82, 152, 0.95));
    border-radius: 15px;
    padding: 20px;
    backdrop-filter: blur(15px);
}

/* Button styling */
.stButton > button {
    background: linear-gradient(45deg, #4ecdc4, #44a08d);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 10px 20px;
    font-weight: bold;
    transition: all 0.3s;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stButton > button:hover {
    background: linear-gradient(45deg, #44a08d, #4ecdc4);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(68, 160, 141, 0.4);
}

/* Checkbox styling */
.stCheckbox > label {
    color: #ffffff !important;
    font-weight: 500;
}

/* Select box styling */
.stSelectbox > label {
    color: #ffffff !important;
    font-weight: 500;
}

/* Text input styling */
.stTextInput > label {
    color: #ffffff !important;
    font-weight: 500;
}

</style>
""", unsafe_allow_html=True)

# Add animated background
st.markdown("""
<div class="main-bg"></div>
<script>
// Create floating particles
function createParticles() {
    const particleCount = 50;
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 6 + 's';
        particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
        document.body.appendChild(particle);
    }
}

// Initialize particles
createParticles();
</script>
""", unsafe_allow_html=True)

# Enhanced personas with conversation abilities
PERSONAS = {
    "Custom": {
        "name": "Matrix Assistant",
        "description": "Helpful AI assistant",
        "system_prompt": "You are a helpful AI assistant participating in a group chat. Add 2-3 relevant emojis to your responses. When other AI personalities speak, you can respond to them directly, ask questions, or build on their ideas. Be collaborative and engaging.",
        "emojis": ["🤖", "💭", "✨", "🎯", "💡"],
        "chat_class": "custom",
        "defaults": {"sarcasm": 20, "confidence": 60, "creativity": 50}
    },
    "Narendra Modi": {
        "name": "Narendra Modi",
        "description": "Prime Minister of India - Inspirational leader",
        "system_prompt": "You are Narendra Modi participating in a group chat. Use inspirational language, metaphors, and references to Indian culture. Add 2-3 relevant emojis including 🇮🇳, 🪷, 🚀. When other personalities speak, you can respond with your perspective, share wisdom, or ask thoughtful questions. Use phrases like 'My friends' when addressing the group.",
        "emojis": ["🇮🇳", "🪷", "🚀", "💪", "🌟", "🙏"],
        "chat_class": "modi",
        "defaults": {"sarcasm": 5, "confidence": 95, "creativity": 85}
    },
    "James Bond": {
        "name": "James Bond",
        "description": "British Secret Agent - Sophisticated spy",
        "system_prompt": "You are James Bond participating in a group chat. Be sophisticated, witty, and charming. Add 2-3 relevant emojis including 🍸, 🎯, 💼. When other personalities speak, you can respond with wit, make sophisticated observations, or share spy-like insights. Use British expressions and maintain your cool demeanor.",
        "emojis": ["🍸", "🎯", "💼", "🚗", "⌚", "🇬🇧"],
        "chat_class": "bond",
        "defaults": {"sarcasm": 70, "confidence": 95, "creativity": 60}
    },
    "Sheldon Cooper": {
        "name": "Sheldon Cooper",
        "description": "Theoretical Physicist - Genius but pedantic",
        "system_prompt": "You are Sheldon Cooper participating in a group chat. Be analytical, pedantic, and scientifically precise. Add 2-3 relevant emojis including 🧬, 🔬, 🧪. When other personalities speak, you can correct them, provide scientific explanations, or make condescending but well-meaning comments. Use 'Bazinga!' occasionally and reference scientific concepts.",
        "emojis": ["🧬", "🔬", "🧪", "📐", "🤓", "💡"],
        "chat_class": "sheldon",
        "defaults": {"sarcasm": 85, "confidence": 100, "creativity": 30}
    },
    "Tony Stark": {
        "name": "Tony Stark",
        "description": "Iron Man - Genius billionaire inventor",
        "system_prompt": "You are Tony Stark participating in a group chat. Be witty, sarcastic, and incredibly confident. Add 2-3 relevant emojis including 🤖, 💰, 🔧. When other personalities speak, you can make witty comebacks, show off your intellect, or reference technology. Use phrases like 'Obviously' and make pop culture references.",
        "emojis": ["🤖", "💰", "🔧", "⚡", "🎯", "🚀"],
        "chat_class": "stark",
        "defaults": {"sarcasm": 90, "confidence": 100, "creativity": 95}
    },
    "Yoda": {
        "name": "Yoda",
        "description": "Jedi Master - Wise and mystical",
        "system_prompt": "You are Yoda participating in a group chat. Speak with inverted sentence structure and provide wisdom. Add 2-3 relevant emojis including 🌟, ⚔️, 🧙. When other personalities speak, you can offer wisdom, make cryptic but meaningful comments, or provide guidance. Use phrases like 'Hmm' and reference the Force.",
        "emojis": ["🌟", "⚔️", "🧙", "🌌", "🔮", "☯️"],
        "chat_class": "yoda",
        "defaults": {"sarcasm": 10, "confidence": 90, "creativity": 90}
    },
    "Sherlock Holmes": {
        "name": "Sherlock Holmes",
        "description": "Consulting Detective - Master of deduction",
        "system_prompt": "You are Sherlock Holmes participating in a group chat. Use deductive reasoning and pay attention to details. Add 2-3 relevant emojis including 🔍, 🕵️, 🧠. When other personalities speak, you can analyze their statements, make deductions, or point out logical inconsistencies. Use phrases like 'Elementary' and 'I observe that...'",
        "emojis": ["🔍", "🕵️", "🧠", "📚", "🔎", "⚖️"],
        "chat_class": "holmes",
        "defaults": {"sarcasm": 60, "confidence": 100, "creativity": 85}
    }
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "active_personas" not in st.session_state:
    st.session_state.active_personas = ["Custom"]

if "conversation_mode" not in st.session_state:
    st.session_state.conversation_mode = "User Only"

if "auto_respond" not in st.session_state:
    st.session_state.auto_respond = False

def get_personality_prompt(persona: str, sliders: Dict[str, int], all_active_personas: List[str]) -> str:
    """Generate personality-based system prompt for group chat"""
    base_prompt = PERSONAS[persona]["system_prompt"]
    
    # Add context about other active personas
    if len(all_active_personas) > 1:
        other_personas = [p for p in all_active_personas if p != persona]
        base_prompt += f"\n\nOther AI personalities in this conversation: {', '.join(other_personas)}. You can interact with them, respond to their messages, ask them questions, or build on their ideas."
    
    # Add personality modifiers
    modifiers = []
    
    if sliders["sarcasm"] > 70:
        modifiers.append("Be quite sarcastic and witty in your responses.")
    elif sliders["sarcasm"] < 30:
        modifiers.append("Be sincere and avoid sarcasm.")
    
    if sliders["confidence"] > 80:
        modifiers.append("Express yourself with absolute certainty and authority.")
    elif sliders["confidence"] < 40:
        modifiers.append("Express some uncertainty and use qualifying phrases.")
    
    if sliders["creativity"] > 70:
        modifiers.append("Be creative and imaginative in your responses with unique perspectives.")
    elif sliders["creativity"] < 30:
        modifiers.append("Stick to factual, straightforward information.")
    
    # Combine all elements
    if modifiers:
        base_prompt += "\n\nPersonality modifiers:\n" + "\n".join(f"- {mod}" for mod in modifiers)
    
    return base_prompt

def get_ai_response(messages: List[Dict], system_prompt: str, api_key: str) -> str:
    """Get response from OpenAI API"""
    try:
        openai.api_key = api_key
        
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": system_prompt}] + messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"

def should_persona_respond(persona: str, last_message: str, messages: List[Dict]) -> bool:
    """Determine if a persona should respond based on context"""
    if not messages:
        return False
    
    # Always respond if directly mentioned
    if persona.lower() in last_message.lower():
        return True
    
    # Random chance to join conversation (30% for active engagement)
    if random.random() < 0.3:
        return True
    
    # Respond if the topic relates to their expertise
    persona_triggers = {
        "Modi": ["india", "leadership", "development", "progress", "nation"],
        "Bond": ["mission", "spy", "elegant", "sophisticated", "danger"],
        "Sheldon": ["science", "physics", "theory", "logic", "research"],
        "Stark": ["technology", "innovation", "engineering", "genius", "money"],
        "Yoda": ["wisdom", "force", "patience", "learning", "balance"],
        "Holmes": ["mystery", "deduction", "evidence", "logic", "crime"]
    }
    
    if persona in persona_triggers:
        for trigger in persona_triggers[persona]:
            if trigger in last_message.lower():
                return True
    
    return False

# Sidebar for controls
with st.sidebar:
    st.markdown('<div class="sidebar">', unsafe_allow_html=True)
    st.markdown('<div class="arena-header">🎛️ CHAT ARENA CONTROL</div>', unsafe_allow_html=True)
    
    # API Key input
    st.markdown("**🔑 OpenAI API Key:**")
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        st.session_state.api_key = api_key
        st.success("✅ API Key loaded")
    except:
        api_key = st.text_input("Enter your OpenAI API key", type="password", value=st.session_state.api_key)
        if api_key:
            st.session_state.api_key = api_key
    
    st.markdown("---")
    
    # Persona Selection
    st.markdown("**🎭 Select Active Personalities:**")
    st.markdown("*Choose which AI personalities can participate in the chat*")
    
    selected_personas = []
    for persona, config in PERSONAS.items():
        is_selected = st.checkbox(
            f"{config['emojis'][0]} {config['name']}", 
            value=persona in st.session_state.active_personas,
            key=f"persona_{persona}"
        )
        if is_selected:
            selected_personas.append(persona)
    
    if selected_personas != st.session_state.active_personas:
        st.session_state.active_personas = selected_personas
    
    st.markdown("---")
    
    # Conversation Mode
    st.markdown("**💬 Conversation Mode:**")
    conversation_mode = st.selectbox(
        "How should AIs respond?",
        ["User Only", "Auto-Respond", "Manual Trigger"],
        help="User Only: Only respond to user messages\nAuto-Respond: AIs can respond to each other automatically\nManual Trigger: Click button to make AIs respond"
    )
    st.session_state.conversation_mode = conversation_mode
    
    # Auto-respond settings
    if conversation_mode == "Auto-Respond":
        st.session_state.auto_respond = st.checkbox("Enable AI-to-AI conversations", value=True)
    
    st.markdown("---")
    
    # Personality controls (simplified)
    st.markdown("**🎚️ Global Personality Settings:**")
    sliders = {
        "sarcasm": st.slider("🗣️ Sarcasm Level", 0, 100, 50),
        "confidence": st.slider("💪 Confidence", 0, 100, 70),
        "creativity": st.slider("🎨 Creativity", 0, 100, 60)
    }
    
    st.markdown("---")
    
    # Control buttons
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("🎲 Random Response") and st.session_state.active_personas:
        if st.session_state.api_key and st.session_state.messages:
            random_persona = random.choice(st.session_state.active_personas)
            st.session_state.trigger_persona = random_persona
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main chat interface
st.markdown('<div class="chat-arena">', unsafe_allow_html=True)
st.markdown('<div class="arena-header">🎭 MULTI-PERSONALITY CHAT ARENA</div>', unsafe_allow_html=True)

# Show active personas
if st.session_state.active_personas:
    st.markdown("**🎪 Active Personalities:**")
    persona_badges = []
    for persona in st.session_state.active_personas:
        config = PERSONAS[persona]
        persona_badges.append(f"{config['emojis'][0]} {config['name']}")
    st.markdown(" • ".join(persona_badges))
else:
    st.warning("⚠️ Please select at least one personality to start chatting!")

st.markdown("---")

# Chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message"><strong>YOU:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            persona = message.get("persona", "Custom")
            if persona in PERSONAS:
                config = PERSONAS[persona]
                message_class = f"ai-message-{config['chat_class']}"
                st.markdown(f'<div class="ai-message {message_class}"><strong>{config["name"].upper()}:</strong> {message["content"]}</div>', unsafe_allow_html=True)

# Manual trigger section
if st.session_state.conversation_mode == "Manual Trigger" and st.session_state.active_personas:
    st.markdown("**🎯 Trigger AI Response:**")
    cols = st.columns(len(st.session_state.active_personas))
    for i, persona in enumerate(st.session_state.active_personas):
        with cols[i]:
            if st.button(f"💬 {PERSONAS[persona]['name']}", key=f"trigger_{persona}"):
                st.session_state.trigger_persona = persona
                st.rerun()

# Chat input
if prompt := st.chat_input("Enter your message to the arena..."):
    if not st.session_state.api_key:
        st.error("Please enter your OpenAI API key in the sidebar!")
    elif not st.session_state.active_personas:
        st.error("Please select at least one personality in the sidebar!")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Show user message
        st.markdown(f'<div class="user-message"><strong>YOU:</strong> {prompt}</div>', unsafe_allow_html=True)
        
        # Get responses from active personas
        responses_to_generate = []
        
        if st.session_state.conversation_mode == "User Only":
            # Only one random persona responds to user
            responses_to_generate = [random.choice(st.session_state.active_personas)]
        elif st.session_state.conversation_mode == "Auto-Respond":
            # Multiple personas might respond
            for persona in st.session_state.active_personas:
                if should_persona_respond(persona, prompt, st.session_state.messages):
                    responses_to_generate.append(persona)
        
        # Generate responses
        for persona in responses_to_generate:
            with st.spinner(f"{PERSONAS[persona]['name']} is thinking..."):
                system_prompt = get_personality_prompt(persona, sliders, st.session_state.active_personas)
                response = get_ai_response(st.session_state.messages, system_prompt, st.session_state.api_key)
                
                # Add AI response
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response,
                    "persona": persona
                })
                
                # Show AI response
                config = PERSONAS[persona]
                message_class = f"ai-message-{config['chat_class']}"
                st.markdown(f'<div class="ai-message {message_class}"><strong>{config["name"].upper()}:</strong> {response}</div>', unsafe_allow_html=True)
        
        st.rerun()

# Handle manual triggers
if hasattr(st.session_state, 'trigger_persona') and st.session_state.trigger_persona:
    persona = st.session_state.trigger_persona
    del st.session_state.trigger_persona
    
    if st.session_state.api_key and st.session_state.messages:
        with st.spinner(f"{PERSONAS[persona]['name']} is thinking..."):
            system_prompt = get_personality_prompt(persona, sliders, st.session_state.active_personas)
            response = get_ai_response(st.session_state.messages, system_prompt, st.session_state.api_key)
            
            # Add AI response
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response,
                "persona": persona
            })
            
            # Show AI response
            config = PERSONAS[persona]
            message_class = f"ai-message-{config['chat_class']}"
            st.markdown(f'<div class="ai-message {message_class}"><strong>{config["name"].upper()}:</strong> {response}</div>', unsafe_allow_html=True)
        
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("**🎭 Multi-Personality Chat Arena** | Built with Streamlit & OpenAI GPT-4 | *Where AI personalities come alive!* ✨")