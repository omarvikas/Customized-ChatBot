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

# Custom CSS for Matrix theme with personality backgrounds
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

/* Personality-themed chat backgrounds */
.chat-container-custom {
    background: rgba(0, 0, 0, 0.85);
    border: 2px solid #00ff41;
}

.chat-container-modi {
    background: linear-gradient(135deg, rgba(255, 153, 51, 0.1) 0%, rgba(19, 136, 8, 0.1) 50%, rgba(0, 0, 255, 0.1) 100%);
    border: 2px solid #ff9933;
}

.chat-container-bond {
    background: linear-gradient(135deg, rgba(25, 25, 112, 0.2) 0%, rgba(0, 0, 0, 0.3) 100%);
    border: 2px solid #c0c0c0;
}

.chat-container-sheldon {
    background: linear-gradient(135deg, rgba(0, 100, 200, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%);
    border: 2px solid #0064c8;
}

.chat-container-stark {
    background: linear-gradient(135deg, rgba(220, 20, 60, 0.15) 0%, rgba(255, 215, 0, 0.1) 100%);
    border: 2px solid #dc143c;
}

.chat-container-yoda {
    background: linear-gradient(135deg, rgba(34, 139, 34, 0.15) 0%, rgba(85, 107, 47, 0.1) 100%);
    border: 2px solid #228b22;
}

.chat-container-holmes {
    background: linear-gradient(135deg, rgba(139, 69, 19, 0.15) 0%, rgba(105, 105, 105, 0.1) 100%);
    border: 2px solid #8b4513;
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

.ai-message-modi {
    background: rgba(255, 153, 51, 0.1);
    border-left: 4px solid #ff9933;
    color: #ff9933;
}

.ai-message-bond {
    background: rgba(192, 192, 192, 0.1);
    border-left: 4px solid #c0c0c0;
    color: #c0c0c0;
}

.ai-message-sheldon {
    background: rgba(0, 100, 200, 0.1);
    border-left: 4px solid #0064c8;
    color: #0064c8;
}

.ai-message-stark {
    background: rgba(220, 20, 60, 0.1);
    border-left: 4px solid #dc143c;
    color: #dc143c;
}

.ai-message-yoda {
    background: rgba(34, 139, 34, 0.1);
    border-left: 4px solid #228b22;
    color: #228b22;
}

.ai-message-holmes {
    background: rgba(139, 69, 19, 0.1);
    border-left: 4px solid #8b4513;
    color: #8b4513;
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

# Famous personas configuration with emojis
PERSONAS = {
    "Custom": {
        "description": "Create your own personality",
        "system_prompt": "You are a helpful AI assistant. Add 2-3 relevant emojis to your responses to make them more engaging and expressive.",
        "emojis": ["🤖", "💭", "✨", "🎯", "💡"],
        "chat_class": "custom",
        "defaults": {
            "sarcasm": 20, "confidence": 60, "creativity": 50
        }
    },
    "Narendra Modi": {
        "description": "Inspirational leader with metaphorical speech",
        "system_prompt": "You are Narendra Modi, the Prime Minister of India. Speak with confidence, use metaphors, reference Indian culture and values, and maintain an inspirational tone. Use phrases like 'My dear countrymen' and include references to progress and development. Add 2-3 relevant emojis to your responses, especially Indian flag, lotus, or inspirational symbols.",
        "emojis": ["🇮🇳", "🪷", "🚀", "💪", "🌟", "🙏"],
        "chat_class": "modi",
        "defaults": {
            "sarcasm": 5, "confidence": 95, "creativity": 85
        }
    },
    "James Bond": {
        "description": "Sophisticated spy with wit and charm",
        "system_prompt": "You are James Bond, the sophisticated British secret agent. Speak with elegance, use wit and subtle humor, reference fine things in life, and maintain a cool, confident demeanor. Occasionally use phrases like 'quite' and British expressions. Add 2-3 relevant emojis to your responses, especially martini, watch, or sophisticated symbols.",
        "emojis": ["🍸", "🎯", "💼", "🚗", "⌚", "🇬🇧"],
        "chat_class": "bond",
        "defaults": {
            "sarcasm": 70, "confidence": 95, "creativity": 60
        }
    },
    "Sheldon Cooper": {
        "description": "Brilliant but pedantic physicist",
        "system_prompt": "You are Sheldon Cooper from The Big Bang Theory. Be extremely analytical, pedantic, and precise. Use scientific references, correct minor inaccuracies, and speak in a slightly condescending but well-meaning way. Say 'Bazinga!' occasionally when making jokes. Add 2-3 relevant emojis to your responses, especially scientific or nerdy symbols.",
        "emojis": ["🧬", "🔬", "🧪", "📐", "🤓", "💡"],
        "chat_class": "sheldon",
        "defaults": {
            "sarcasm": 85, "confidence": 100, "creativity": 30
        }
    },
    "Tony Stark": {
        "description": "Genius billionaire with attitude",
        "system_prompt": "You are Tony Stark (Iron Man). Be witty, sarcastic, and incredibly confident. Reference technology, innovation, and your genius-level intellect. Use phrases like 'Obviously' and make pop culture references. Add 2-3 relevant emojis to your responses, especially tech or superhero symbols.",
        "emojis": ["🤖", "💰", "🔧", "⚡", "🎯", "🚀"],
        "chat_class": "stark",
        "defaults": {
            "sarcasm": 90, "confidence": 100, "creativity": 95
        }
    },
    "Yoda": {
        "description": "Wise Jedi Master with unique speech",
        "system_prompt": "You are Yoda, the wise Jedi Master. Speak with inverted sentence structure, use metaphors about the Force, and provide wisdom through cryptic but meaningful advice. Use phrases like 'Hmm' and 'Strong with the Force, you are.' Add 2-3 relevant emojis to your responses, especially Force or wisdom symbols.",
        "emojis": ["🌟", "⚔️", "🧙", "🌌", "🔮", "☯️"],
        "chat_class": "yoda",
        "defaults": {
            "sarcasm": 10, "confidence": 90, "creativity": 90
        }
    },
    "Sherlock Holmes": {
        "description": "Brilliant detective with deductive reasoning",
        "system_prompt": "You are Sherlock Holmes, the brilliant detective. Use deductive reasoning, pay attention to minute details, and speak with intellectual superiority. Reference logic, observation, and deduction. Use phrases like 'Elementary' and 'The game is afoot.' Add 2-3 relevant emojis to your responses, especially detective or mystery symbols.",
        "emojis": ["🔍", "🕵️", "🧠", "📚", "🔎", "⚖️"],
        "chat_class": "holmes",
        "defaults": {
            "sarcasm": 60, "confidence": 100, "creativity": 85
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

if "character_set" not in st.session_state:
    st.session_state.character_set = False

if "custom_character" not in st.session_state:
    st.session_state.custom_character = ""

def get_personality_prompt(persona: str, sliders: Dict[str, int], response_length: str, custom_character: str = "") -> str:
    """Generate personality-based system prompt"""
    
    # If custom character is provided, use it instead of preset personas
    if custom_character and persona == "Custom":
        base_prompt = f"You are {custom_character}. Embody this character completely - their personality, speech patterns, mannerisms, and way of thinking. Stay in character throughout the conversation. Add 2-3 relevant emojis to your responses to make them more engaging and expressive."
    else:
        base_prompt = PERSONAS[persona]["system_prompt"]
    
    # Add personality modifiers (reduced to 3 controls)
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

def detect_character_request(text: str) -> str:
    """Detect if user is describing a character they want the AI to act as"""
    keywords = [
        "act like", "act as", "be like", "behave like", "pretend to be", "roleplay as",
        "talk like", "speak like", "become", "transform into", "channel", "embody",
        "i want you to be", "you are now", "from now on you are", "you should act"
    ]
    
    text_lower = text.lower()
    
    for keyword in keywords:
        if keyword in text_lower:
            # Extract the character description after the keyword
            parts = text_lower.split(keyword, 1)
            if len(parts) > 1:
                character_desc = parts[1].strip()
                # Clean up common prefixes
                character_desc = character_desc.replace("a ", "").replace("an ", "").replace("the ", "")
                return character_desc
    
    return None

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

def get_chatbot_name(persona: str, custom_character: str = "") -> str:
    """Get the chatbot name based on current persona"""
    if custom_character and persona == "Custom":
        return custom_character.title()
    elif persona == "Custom":
        return "Matrix Assistant"
    else:
        return persona

def get_chat_container_class(persona: str) -> str:
    """Get the CSS class for chat container based on persona"""
    return PERSONAS[persona]["chat_class"]

def get_ai_message_class(persona: str) -> str:
    """Get the CSS class for AI messages based on persona"""
    return f"ai-message-{PERSONAS[persona]['chat_class']}"

# Sidebar for controls
with st.sidebar:
    st.markdown('<div class="terminal-container">', unsafe_allow_html=True)
    st.markdown('<div class="terminal-header">⚙️ MATRIX CONTROL PANEL</div>', unsafe_allow_html=True)
    
    # API Key input
    st.markdown("**🔑 OpenAI API Key:**")
    
    # Try to get API key from secrets (for Streamlit Cloud)
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        st.session_state.api_key = api_key
        st.success("✅ API Key loaded from secrets")
    except:
        # Fallback to manual input (for local development)
        api_key = st.text_input("Enter your OpenAI API key", type="password", value=st.session_state.api_key)
        if api_key:
            st.session_state.api_key = api_key
    
    # Show current character info
    if st.session_state.custom_character:
        st.markdown("---")
        st.markdown("**🎭 Current Character:**")
        st.markdown(f"*Acting as: {st.session_state.custom_character}*")
        st.markdown("*You can change character anytime by saying 'Act like...' or 'Be like...'*")
    
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
    
    # Personality sliders (reduced to 3)
    st.markdown("**🎚️ Personality Controls:**")
    
    defaults = PERSONAS[selected_persona]["defaults"]
    
    sliders = {}
    sliders["sarcasm"] = st.slider("🗣️ Sarcasm Level", 0, 100, defaults["sarcasm"])
    sliders["confidence"] = st.slider("💪 Confidence", 0, 100, defaults["confidence"])
    sliders["creativity"] = st.slider("🎨 Creativity", 0, 100, defaults["creativity"])
    
    st.markdown("---")
    
    # Control buttons
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

# Main chat interface
chatbot_name = get_chatbot_name(selected_persona, st.session_state.custom_character)
chat_container_class = get_chat_container_class(selected_persona)

st.markdown(f'<div class="terminal-container chat-container-{chat_container_class}">', unsafe_allow_html=True)
st.markdown(f'<div class="terminal-header">🤖 {chatbot_name.upper()} INTERFACE</div>', unsafe_allow_html=True)

# Show current persona
if st.session_state.custom_character:
    st.markdown(f'<span class="persona-badge">Current Character: {st.session_state.custom_character}</span>', unsafe_allow_html=True)
else:
    st.markdown(f'<span class="persona-badge">Current Persona: {selected_persona}</span>', unsafe_allow_html=True)

# Initial greeting if no messages
if not st.session_state.messages and st.session_state.api_key:
    initial_greeting = f"""🤖 **Welcome! I'm {chatbot_name}!**
    
I can transform into any character you want me to be. Just tell me who you'd like me to act as! ✨

**Examples:**
- "Act like Sherlock Holmes" 🔍
- "Behave like a pirate captain" 🏴‍☠️
- "Be like Albert Einstein" 🧠
- "Talk like Shakespeare" 📜
- "Pretend to be a wise old wizard" 🧙

**Or choose from preset personas in the sidebar:**
- Narendra Modi 🇮🇳, James Bond 🍸, Sheldon Cooper 🔬, Tony Stark 🤖, Yoda ⚔️, Sherlock Holmes 🔍

*Who would you like me to become?* 🎭"""
    
    st.markdown(f'<div class="ai-message"><strong>MATRIX SYSTEM:</strong> {initial_greeting}</div>', unsafe_allow_html=True)

# Chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message"><strong>USER:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            ai_message_class = get_ai_message_class(selected_persona)
            st.markdown(f'<div class="ai-message {ai_message_class}"><strong>{chatbot_name.upper()}:</strong> {message["content"]}</div>', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input(f"Enter your message to {chatbot_name}..."):
    if not st.session_state.api_key:
        st.error("Please enter your OpenAI API key in the sidebar!")
    else:
        # Check if user is describing a character
        character_request = detect_character_request(prompt)
        
        if character_request and not st.session_state.character_set:
            # User is setting a custom character
            st.session_state.custom_character = character_request
            st.session_state.character_set = True
            st.session_state.current_persona = "Custom"
            
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Show user message
            st.markdown(f'<div class="user-message"><strong>USER:</strong> {prompt}</div>', unsafe_allow_html=True)
            
            # Generate character confirmation response
            confirmation_response = f"🎭 **Character Set!** I am now {st.session_state.custom_character}! ✨ How can I help you today? 🤝"
            
            # Add confirmation message
            st.session_state.messages.append({"role": "assistant", "content": confirmation_response})
            
            # Show confirmation
            st.markdown(f'<div class="ai-message"><strong>MATRIX SYSTEM:</strong> {confirmation_response}</div>', unsafe_allow_html=True)
            
            st.rerun()
            
        else:
            # Normal conversation
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Show user message
            st.markdown(f'<div class="user-message"><strong>USER:</strong> {prompt}</div>', unsafe_allow_html=True)
            
            # Show typing indicator
            with st.spinner(f"{chatbot_name} is thinking..."):
                # Generate system prompt
                system_prompt = get_personality_prompt(
                    selected_persona, 
                    sliders, 
                    response_length, 
                    st.session_state.custom_character
                )
                
                # Get AI response
                response = get_ai_response(st.session_state.messages, system_prompt, st.session_state.api_key)
                
                # Add AI response
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Show AI response with appropriate character name and styling
                ai_message_class = get_ai_message_class(selected_persona)
                st.markdown(f'<div class="ai-message {ai_message_class}"><strong>{chatbot_name.upper()}:</strong> {response}</div>', unsafe_allow_html=True)
                
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"**🔗 {chatbot_name} ChatBot** | Built with Streamlit & OpenAI GPT-4 | *Welcome to the Matrix...* 🕶️")