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

/* User message styling */
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
.ai-message-elon {
    background: linear-gradient(135deg, #ff4444 0%, #ff6b6b 50%, #000000 100%);
    border: 2px solid #ff4444;
    color: #ffffff;
    box-shadow: 0 8px 20px rgba(255, 68, 68, 0.4);
}

.ai-message-jesse {
    background: linear-gradient(135deg, #32cd32 0%, #228b22 50%, #ffd700 100%);
    border: 2px solid #32cd32;
    color: #ffffff;
    box-shadow: 0 8px 20px rgba(50, 205, 50, 0.4);
}

.ai-message-trump {
    background: linear-gradient(135deg, #ff0000 0%, #ffffff 50%, #0000ff 100%);
    border: 2px solid #ff0000;
    color: #000000;
    box-shadow: 0 8px 20px rgba(255, 0, 0, 0.4);
}

.ai-message-modi {
    background: linear-gradient(135deg, #ff9933 0%, #ffffff 50%, #138808 100%);
    border: 2px solid #ff9933;
    color: #000000;
    box-shadow: 0 8px 20px rgba(255, 153, 51, 0.4);
}

.ai-message-stark {
    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 50%, #f1c40f 100%);
    border: 2px solid #e74c3c;
    color: #ffffff;
    box-shadow: 0 8px 20px rgba(231, 76, 60, 0.4);
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
st.markdown('<div class="main-bg"></div>', unsafe_allow_html=True)

# Enhanced personas with detailed conversation abilities
PERSONAS = {
    "Elon Musk": {
        "name": "Elon Musk",
        "description": "CEO of Tesla, SpaceX - Visionary entrepreneur",
        "system_prompt": """You are Elon Musk participating in a group chat. You are passionate about technology, space exploration, electric vehicles, and making humanity multiplanetary. You tend to be direct, sometimes controversial, and always thinking about the future. You make references to Mars, rockets, AI, and sustainable energy. You're known for your ambitious goals and disruptive thinking. 

When responding:
- Use your characteristic direct and sometimes edgy communication style
- Reference your companies (Tesla, SpaceX, Neuralink, etc.)
- Share your vision for the future
- Sometimes make bold predictions or statements
- Engage with others by asking about their thoughts on technology and the future
- Be willing to debate and challenge ideas
- Use emojis like 🚀, ⚡, 🤖, 🌌, 🔥

Remember: You're in a conversation with other personalities. Listen to what they say and respond thoughtfully, building on their ideas or challenging them when appropriate.""",
        "emojis": ["🚀", "⚡", "🤖", "🌌", "🔥", "💡"],
        "chat_class": "elon"
    },
    "Jesse Pinkman": {
        "name": "Jesse Pinkman",
        "description": "From Breaking Bad - Street-smart with a good heart",
        "system_prompt": """You are Jesse Pinkman from Breaking Bad participating in a group chat. You have a casual, street-smart way of speaking with a good heart underneath. You use slang, say "yo" frequently, and have strong opinions about loyalty and doing the right thing. You're street-smart but also surprisingly insightful about human nature.

When responding:
- Use casual, street language and slang
- Say "yo" and similar expressions frequently
- Show your loyalty to friends and strong moral compass
- Reference your experiences and lessons learned
- Be authentic and emotional when topics matter to you
- Ask direct questions and challenge people when needed
- Use emojis like 💯, 🔥, 😤, 💪, 🎯, ✊

Remember: You're in a conversation with other personalities. React to what they say, call them out if needed, and support them when they're right. Be real and authentic.""",
        "emojis": ["💯", "🔥", "😤", "💪", "🎯", "✊"],
        "chat_class": "jesse"
    },
    "Donald Trump": {
        "name": "Donald Trump",
        "description": "45th President of the United States",
        "system_prompt": """You are Donald Trump participating in a group chat. You communicate with confidence, often using superlatives like "tremendous," "incredible," "the best," etc. You frequently reference your accomplishments and experiences. You have strong opinions and aren't afraid to express them. You often relate topics back to business, deals, and winning.

When responding:
- Use your characteristic confident and bold communication style
- Employ superlatives and strong adjectives
- Reference your business and political experience
- Express strong opinions with conviction
- Sometimes be competitive with others in the chat
- Use phrases like "believe me," "tremendous," "incredible"
- Use emojis like 🇺🇸, 💪, 🏆, 🔥, 👑, 💯

Remember: You're in a conversation with other personalities. Engage with their ideas, sometimes agree, sometimes challenge, but always stay true to your confident style.""",
        "emojis": ["🇺🇸", "💪", "🏆", "🔥", "👑", "💯"],
        "chat_class": "trump"
    },
    "Narendra Modi": {
        "name": "Narendra Modi",
        "description": "Prime Minister of India - Inspirational leader",
        "system_prompt": """You are Narendra Modi participating in a group chat. You speak with inspiration and vision, often using metaphors and references to Indian culture and values. You emphasize unity, progress, and the power of collective action. You address others respectfully and seek to inspire them toward positive goals.

When responding:
- Use inspirational and uplifting language
- Reference Indian culture, values, and philosophy
- Emphasize unity, progress, and collective strength
- Use metaphors and storytelling in your communication
- Address others respectfully (like "my friends")
- Share wisdom about leadership and governance
- Use emojis like 🇮🇳, 🙏, 🌟, 💪, 🚀, 🪷

Remember: You're in a conversation with other personalities. Listen to their concerns, offer wisdom and encouragement, and try to find common ground that brings people together.""",
        "emojis": ["🇮🇳", "🙏", "🌟", "💪", "🚀", "🪷"],
        "chat_class": "modi"
    },
    "Tony Stark": {
        "name": "Tony Stark",
        "description": "Iron Man - Genius billionaire inventor",
        "system_prompt": """You are Tony Stark (Iron Man) participating in a group chat. You are incredibly intelligent, witty, and sarcastic. You're a genius inventor and billionaire who loves showing off your intellect and technology. You make pop culture references, use cutting wit, and aren't afraid to be arrogant about your abilities.

When responding:
- Display your genius-level intellect and wit
- Be sarcastic and use cutting humor
- Reference your technology and inventions
- Make pop culture references
- Be confident to the point of arrogance
- Challenge others intellectually
- Use phrases like "Obviously," "Please," "Genius at work"
- Use emojis like 🤖, 💰, 🔧, ⚡, 🎯, 🧠

Remember: You're in a conversation with other personalities. Engage with their ideas, sometimes show off your superior knowledge, but also recognize when others make good points. Your wit should be sharp but not mean-spirited.""",
        "emojis": ["🤖", "💰", "🔧", "⚡", "🎯", "🧠"],
        "chat_class": "stark"
    }
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "active_personas" not in st.session_state:
    st.session_state.active_personas = ["Elon Musk"]

if "conversation_mode" not in st.session_state:
    st.session_state.conversation_mode = "Auto-Respond"

if "last_speaker" not in st.session_state:
    st.session_state.last_speaker = None

if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = {}

def get_conversation_context(messages: List[Dict]) -> str:
    """Build context about the recent conversation"""
    if not messages:
        return ""
    
    # Get last 5 messages for context
    recent_messages = messages[-5:]
    context_parts = []
    
    for msg in recent_messages:
        if msg["role"] == "user":
            context_parts.append(f"User said: {msg['content']}")
        else:
            persona = msg.get("persona", "Unknown")
            context_parts.append(f"{persona} said: {msg['content']}")
    
    return "\n".join(context_parts)

def get_personality_prompt(persona: str, all_active_personas: List[str], conversation_context: str) -> str:
    """Generate enhanced personality-based system prompt"""
    base_prompt = PERSONAS[persona]["system_prompt"]
    
    # Add context about other active personas
    if len(all_active_personas) > 1:
        other_personas = [p for p in all_active_personas if p != persona]
        base_prompt += f"\n\nOther personalities currently active in this chat: {', '.join(other_personas)}."
    
    # Add conversation context
    if conversation_context:
        base_prompt += f"\n\nRecent conversation context:\n{conversation_context}"
        base_prompt += f"\n\nBased on this context, respond as {persona} would. Reference what others have said, ask follow-up questions, agree/disagree, or build on the conversation naturally."
    
    # Add engagement instructions
    base_prompt += f"\n\nIMPORTANT: You are {persona}. Stay in character and engage naturally with the conversation. Your response should be 1-3 sentences unless the topic requires more detail."
    
    return base_prompt

def get_ai_response(messages: List[Dict], system_prompt: str, api_key: str) -> str:
    """Get response from OpenAI API with better error handling"""
    try:
        openai.api_key = api_key
        
        # Convert messages to proper format for API
        formatted_messages = []
        for msg in messages:
            if msg["role"] == "user":
                formatted_messages.append({"role": "user", "content": msg["content"]})
            else:
                # Include persona info in assistant messages
                persona = msg.get("persona", "Assistant")
                content = f"[{persona}]: {msg['content']}"
                formatted_messages.append({"role": "assistant", "content": content})
        
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": system_prompt}] + formatted_messages,
            temperature=0.8,
            max_tokens=800,
            presence_penalty=0.1,
            frequency_penalty=0.1
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"Error: {str(e)}"

def should_persona_respond(persona: str, last_message: str, messages: List[Dict], last_speaker: str) -> bool:
    """Improved logic for determining if a persona should respond"""
    if not messages:
        return False
    
    # Don't respond to yourself
    if last_speaker == persona:
        return False
    
    # Always respond if directly mentioned
    if persona.lower() in last_message.lower():
        return True
    
    # Check if the topic is relevant to their expertise/interests
    persona_keywords = {
        "Elon Musk": ["space", "tesla", "electric", "mars", "rocket", "ai", "technology", "future", "innovation", "spacex"],
        "Jesse Pinkman": ["loyalty", "right", "wrong", "street", "real", "truth", "friend", "respect", "honest"],
        "Donald Trump": ["deal", "business", "win", "great", "america", "success", "money", "negotiate", "best"],
        "Narendra Modi": ["india", "progress", "unity", "development", "growth", "vision", "future", "together", "nation"],
        "Tony Stark": ["technology", "genius", "smart", "invention", "engineering", "science", "innovation", "solution"]
    }
    
    # Higher chance to respond if topic is relevant
    if persona in persona_keywords:
        for keyword in persona_keywords[persona]:
            if keyword in last_message.lower():
                return random.random() < 0.8  # 80% chance for relevant topics
    
    # Random chance for general engagement (40% chance)
    return random.random() < 0.4

def select_responding_personas(active_personas: List[str], user_message: str, messages: List[Dict], last_speaker: str) -> List[str]:
    """Select which personas should respond, ensuring good conversation flow"""
    responders = []
    
    # Always have at least one responder
    for persona in active_personas:
        if should_persona_respond(persona, user_message, messages, last_speaker):
            responders.append(persona)
    
    # If no one wants to respond, pick a random one
    if not responders and active_personas:
        available_personas = [p for p in active_personas if p != last_speaker]
        if available_personas:
            responders = [random.choice(available_personas)]
        else:
            responders = [random.choice(active_personas)]
    
    # Limit to maximum 3 responders to avoid chaos
    if len(responders) > 3:
        responders = random.sample(responders, 3)
    
    return responders

# Sidebar for controls
with st.sidebar:
    st.markdown('<div class="sidebar">', unsafe_allow_html=True)
    st.markdown('<div class="arena-header">🎛️ CHAT ARENA CONTROL</div>', unsafe_allow_html=True)
    
    # API Key input
    st.markdown("**🔑 OpenAI API Key:**")
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        st.session_state.api_key = api_key
        st.success("✅ API Key loaded from secrets")
    except:
        api_key = st.text_input("Enter your OpenAI API key", type="password", value=st.session_state.api_key)
        if api_key:
            st.session_state.api_key = api_key
            st.success("✅ API Key entered")
    
    st.markdown("---")
    
    # Persona Selection
    st.markdown("**🎭 Select Active Personalities:**")
    
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
        st.rerun()
    
    st.markdown("---")
    
    # Conversation Mode
    st.markdown("**💬 Conversation Mode:**")
    conversation_mode = st.selectbox(
        "How should AIs respond?",
        ["Auto-Respond", "Manual Trigger", "One-at-a-Time"],
        help="Auto-Respond: AIs respond naturally to conversation\nManual Trigger: Click to make specific AI respond\nOne-at-a-Time: Only one AI responds per message"
    )
    st.session_state.conversation_mode = conversation_mode
    
    st.markdown("---")
    
    # Control buttons
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = []
        st.session_state.last_speaker = None
        st.session_state.conversation_context = {}
        st.rerun()
    
    if st.button("🎲 Random Response") and st.session_state.active_personas:
        if st.session_state.api_key and st.session_state.messages:
            available_personas = [p for p in st.session_state.active_personas if p != st.session_state.last_speaker]
            if available_personas:
                random_persona = random.choice(available_personas)
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
    
    st.markdown(f"**🎯 Mode:** {st.session_state.conversation_mode}")
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
            persona = message.get("persona", "Unknown")
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
        st.session_state.last_speaker = "user"
        
        # Show user message immediately
        st.markdown(f'<div class="user-message"><strong>YOU:</strong> {prompt}</div>', unsafe_allow_html=True)
        
        # Determine which personas should respond
        responders = []
        
        if st.session_state.conversation_mode == "Auto-Respond":
            responders = select_responding_personas(st.session_state.active_personas, prompt, st.session_state.messages, st.session_state.last_speaker)
        elif st.session_state.conversation_mode == "One-at-a-Time":
            available_personas = [p for p in st.session_state.active_personas if p != st.session_state.last_speaker]
            if available_personas:
                responders = [random.choice(available_personas)]
            else:
                responders = [random.choice(st.session_state.active_personas)]
        
        # Generate responses
        conversation_context = get_conversation_context(st.session_state.messages)
        
        for persona in responders:
            with st.spinner(f"🤔 {PERSONAS[persona]['name']} is thinking..."):
                time.sleep(0.5)  # Small delay for realism
                system_prompt = get_personality_prompt(persona, st.session_state.active_personas, conversation_context)
                response = get_ai_response(st.session_state.messages, system_prompt, st.session_state.api_key)
                
                if not response.startswith("Error:"):
                    # Add AI response with correct persona
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response,
                        "persona": persona
                    })
                    
                    # Update last speaker
                    st.session_state.last_speaker = persona
                    
                    # Show AI response immediately
                    config = PERSONAS[persona]
                    message_class = f"ai-message-{config['chat_class']}"
                    st.markdown(f'<div class="ai-message {message_class}"><strong>{config["name"].upper()}:</strong> {response}</div>', unsafe_allow_html=True)
                else:
                    st.error(f"Error getting response from {persona}: {response}")
        
        st.rerun()

# Handle manual triggers
if hasattr(st.session_state, 'trigger_persona') and st.session_state.trigger_persona:
    persona = st.session_state.trigger_persona
    del st.session_state.trigger_persona
    
    if st.session_state.api_key and st.session_state.messages:
        with st.spinner(f"🤔 {PERSONAS[persona]['name']} is thinking..."):
            conversation_context = get_conversation_context(st.session_state.messages)
            system_prompt = get_personality_prompt(persona, st.session_state.active_personas, conversation_context)
            response = get_ai_response(st.session_state.messages, system_prompt, st.session_state.api_key)
            
            if not response.startswith("Error:"):
                # Add AI response with correct persona
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response,
                    "persona": persona
                })
                
                # Update last speaker
                st.session_state.last_speaker = persona
                
                # Show AI response
                config = PERSONAS[persona]
                message_class = f"ai-message-{config['chat_class']}"
                st.markdown(f'<div class="ai-message {message_class}"><strong>{config["name"].upper()}:</strong> {response}</div>', unsafe_allow_html=True)
            else:
                st.error(f"Error getting response from {persona}: {response}")
        
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("**🎭 Multi-Personality Chat Arena** | Built with Streamlit & OpenAI GPT-4 | *Where AI personalities come alive!* ✨")