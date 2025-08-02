import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import json
import os
import time

# 🌈 Dynamic Color Themes
MOOD_THEMES = {
    "rage": {
        "bg": "linear-gradient(135deg, #400000 0%, #200000 100%)",
        "text": "#ff9999",
        "input": "#ffcccc",
        "input_bg": "#660000",
        "input_border": "#ff4d4d",
        "input_text": "#ffffff",
        "placeholder": "#ffb3b3",
        "card": "rgba(100, 0, 0, 0.7)",
        "border": "#ff4d4d"
    },
    "fury": {
        "bg": "linear-gradient(135deg, #601010 0%, #300808 100%)",
        "text": "#ffb3b3",
        "input": "#ffdddd",
        "input_bg": "#801010",
        "input_border": "#ff6666",
        "input_text": "#ffffff",
        "placeholder": "#ffcccc",
        "card": "rgba(120, 20, 20, 0.7)",
        "border": "#ff6666"
    },
    "calm": {
        "bg": "linear-gradient(135deg, #003366 0%, #001a33 100%)",
        "text": "#ccffff",
        "input": "#e6ffff",
        "input_bg": "#004080",
        "input_border": "#4da6ff",
        "input_text": "#ffffff",
        "placeholder": "#b3e6ff",
        "card": "rgba(0, 60, 100, 0.7)",
        "border": "#4da6ff"
    },
    "funny": {
        "bg": "linear-gradient(135deg, #663366 0%, #331a33 100%)",
        "text": "#ffccff",
        "input": "#ffe6ff",
        "input_bg": "#804080",
        "input_border": "#cc99ff",
        "input_text": "#ffffff",
        "placeholder": "#e6b3ff",
        "card": "rgba(80, 0, 80, 0.7)",
        "border": "#cc99ff"
    },
    "default": {
        "bg": "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
        "text": "#e6f3ff",
        "input": "#ffffff",
        "input_bg": "#2a3f5f",
        "input_border": "#4a6fa5",
        "input_text": "#ffffff",
        "placeholder": "#ccddff",
        "card": "rgba(30, 30, 60, 0.7)",
        "border": "#4a6fa5"
    }
}

# 🎨 Dynamic CSS Styling
def apply_theme(theme):
    st.markdown(f"""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        
        /* Base Styling */
        .stApp {{
            background: {theme['bg']} !important;
            color: {theme['text']} !important;
            font-family: 'Poppins', sans-serif !important;
        }}
        
        /* Input Box Styling */
        .stTextInput > div > div > input {{
            background-color: {theme['input_bg']} !important;
            color: {theme['input_text']} !important;
            border: 2px solid {theme['input_border']} !important;
            border-radius: 12px !important;
            padding: 12px 16px !important;
            font-size: 16px !important;
            font-weight: 400 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        }}
        
        /* Input Box Focus State */
        .stTextInput > div > div > input:focus {{
            border-color: {theme['border']} !important;
            box-shadow: 0 0 0 3px {theme['border']}33 !important;
            outline: none !important;
        }}
        
        /* Input Label Styling */
        .stTextInput > label {{
            color: {theme['text']} !important;
            font-weight: 600 !important;
            font-size: 18px !important;
            margin-bottom: 8px !important;
        }}
        
        /* Placeholder Text */
        .stTextInput > div > div > input::placeholder {{
            color: {theme['placeholder']} !important;
            opacity: 0.7 !important;
        }}
        
        /* Mood Cards */
        .mood-card {{
            color: {theme['text']} !important;
            border-left-color: {theme['border']} !important;
        }}
        
        /* Buttons Styling */
        .stButton > button {{
            background: linear-gradient(45deg, {theme['border']}, {theme['input_border']}) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
        }}
        
        /* Title Styling */
        h1 {{
            background: linear-gradient(45deg, {theme['border']}, {theme['text']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 700 !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        /* Container Styling */
        .main > div {{
            padding-top: 2rem !important;
        }}
        
        /* Warning and Error Messages */
        .stAlert {{
            background-color: {theme['card']} !important;
            color: {theme['text']} !important;
            border-left: 4px solid {theme['border']} !important;
        }}
    </style>
    """, unsafe_allow_html=True)

# 🎤 Voice Recognition Function
def voice_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.session_state.listening = True
        st.write("🎤 Speak now (5 seconds)...")
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)
            return text
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return ""
        finally:
            st.session_state.listening = False

# 🔊 Voice Response
def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("roast.mp3")
        os.system("start roast.mp3")
    except Exception as e:
        st.error(f"Voice error: {str(e)}")

# 🧠 Mood Detection
def load_phrases():
    try:
        with open("phrases.json", encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading phrases: {str(e)}")
        return {
            "angry": {"mood": "Rage 😡", "roast": "Whoa there, hothead! Cool your jets!", "theme": "rage"},
            "mad": {"mood": "Fury 🔥", "roast": "Someone's having a spicy day!", "theme": "fury"},
            "happy": {"mood": "Calm 😊", "roast": "Look at you being all positive!", "theme": "calm"},
            "funny": {"mood": "Funny 😂", "roast": "A comedian in the making!", "theme": "funny"}
        }

def detect_mood(text):
    phrases = load_phrases()
    text_lower = text.lower()
    for phrase in phrases:
        if phrase.lower() in text_lower:
            return phrases[phrase]
    return {"mood": "Calm 😇", "roast": "No strong mood detected, you seem pretty chill!", "theme": "calm"}

# 🖥️ Main App UI
def main():
    # Initialize session state
    if 'current_theme' not in st.session_state:
        st.session_state.current_theme = "default"
    
    # Apply current theme
    current_theme = MOOD_THEMES[st.session_state.current_theme]
    apply_theme(current_theme)
    
    # App Title
    st.markdown('<h1 style="text-align: center; margin-bottom: 2rem;">🎭 MOODROAST 🎭</h1>', unsafe_allow_html=True)

    # Main container
    with st.container():
        # Input field with custom placeholder
        user_input = st.text_input(
            "💬 Share your thoughts:", 
            key="input",
            placeholder="Type your message here or use the speak button..."
        )
        
        # Button row
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🎤 Speak Instead"):
                user_input = voice_to_text()
                if user_input:
                    st.session_state.input = user_input
                    st.rerun()
        
        with col2:
            if st.button("🔥 Analyze Mood"):
                if user_input and user_input.strip():
                    mood_data = detect_mood(user_input)
                    theme_name = mood_data.get("theme", "default")
                    st.session_state.current_theme = theme_name
                    
                    # Get the new theme
                    theme = MOOD_THEMES.get(theme_name, MOOD_THEMES["default"])
                    
                    # Display results with theme-appropriate colors
                    st.markdown(f"""
                    <div style="
                        background: {theme['card']};
                        border-radius: 20px;
                        padding: 2rem;
                        margin: 2rem 0;
                        border-left: 6px solid {theme['border']};
                        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
                        backdrop-filter: blur(10px);
                    ">
                        <h2 style="color: {theme['text']}; margin-bottom: 1rem; font-weight: 600;">{mood_data['mood']}</h2>
                        <p style="color: {theme['text']}; font-size: 1.2rem; margin: 0; line-height: 1.5;">{mood_data['roast']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    speak(mood_data["roast"])
                    time.sleep(10)
                    st.rerun()


                else:
                    st.warning("🤔 Please enter or speak a message first!")
        
        with col3:
            if st.button("🎨 Reset Theme"):
                st.session_state.current_theme = "default"
                st.rerun()

    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; opacity: 0.7; font-size: 0.9rem;'>Speak your mind and let MoodRoast analyze your vibe! 🚀</p>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()