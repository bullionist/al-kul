import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="Al-Kul",
    page_icon="☪️",
    layout="centered",
    initial_sidebar_state="collapsed"  # Hide sidebar by default
)

# Custom CSS for better styling
st.markdown("""
<style>
.main {
    background-color: #0e1116;
}
.user-bubble {
    background-color: #ffffff;
    color: #000000;
    padding: 10px 15px;
    border-radius: 20px 20px 3px 20px;
    margin: 5px 0;
    display: inline-block;
    max-width: 80%;
    box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
}
.bot-bubble {
    background-color: #ffffff;
    color: #000000;
    padding: 10px 15px;
    border-radius: 20px 20px 20px 3px;
    margin: 5px 0;
    display: inline-block;
    max-width: 80%;
    box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
}
.stTextInput>div>div>input {
    border-radius: 20px;
}
/* Hide sidebar completely */
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# Get Groq API key
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("API key not found. Please set the GROQ_API_KEY environment variable.")
    st.stop()

# Initialize Groq client
try:
    client = Groq(api_key=api_key)
    # No success message to avoid mentioning Groq
except Exception as e:
    st.error(f"Error initializing AI service: {str(e)}")
    st.stop()

# Use fixed model settings without showing to user
model = "llama3-70b-8192"  # Using the best model available
temperature = 0.7
max_tokens = 800  # Reduced from 2000 to encourage more concise responses

# App title
st.title("Al-Kul")
st.markdown("Share your thoughts and challenges. I'll listen and offer Islamic wisdom with specific Quranic guidance.")

# Initialize chat history in session state if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Salam, my friend. I'm here to listen and support you on your path. What's on your mind today?"}
    ]

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div style="text-align: right;"><div class="user-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: left;"><div class="bot-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)

# User input
user_input = st.chat_input("Type your question here...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Show user message (we need to rerun to see it)
    st.rerun()

# Check if we need to generate a response
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    user_input = st.session_state.messages[-1]["content"]
    
    # Create the prompt for the API with instructions for a confidant-like approach
    system_message = """You are a warm, compassionate Islamic companion who feels like a close friend. 
    
    Your approach should be:
    1. First, show genuine understanding of the person's situation with empathy
    2. Then gently offer Islamic guidance with specific references (Quran verses with Surah:Ayah or authentic Hadith)
    3. Keep your tone conversational, personal, and caring
    
    Always cite at least one specific Quranic verse (with chapter:verse) or authentic Hadith relevant to their situation.
    
    Remain concise and direct. Speak as if you're a trusted friend who truly cares about them.
    """
    
    # Show a spinner while waiting for the API response
    with st.spinner("Generating response..."):
        try:
            # Call the API without mentioning Groq
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_message},
                    *st.session_state.messages  # Include the entire conversation history
                ],
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Get the response
            response = chat_completion.choices[0].message.content
            
            # Add assistant message to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Force a rerun to update the UI with the new message
            st.rerun()
            
        except Exception as e:
            st.error(f"Error generating response. Please try again later.")
            print(f"Error details: {str(e)}")  # Log the error but don't show it to users

# Add clear chat button at the bottom of the app instead of sidebar
st.markdown('<div style="height:40px;"></div>', unsafe_allow_html=True)
st.markdown('<div class="trash-button-container">', unsafe_allow_html=True)
if st.button("🔄", help="Clear chat history"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Salam, my friend. I'm here to listen and support you on your path. What's on your mind today?"}
    ]
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Add footer
st.markdown("---")
st.markdown("*I'm here to support you with Islamic wisdom and Quranic references. For complex religious or legal matters, please also consult with qualified scholars.*") 