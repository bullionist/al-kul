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
    background-color: #f5f5f5;
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
max_tokens = 2000

# App title
st.title("Al-Kul")
st.markdown("Ask questions about personal challenges and receive advice rooted in Islamic teachings.")

# Initialize chat history in session state if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Assalamu alaikum! How can I assist you with Islamic guidance today?"}
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
    
    # Create the prompt for the API
    system_message = "You are an Islamic guidance assistant that provides advice based on Islamic teachings, Quran, and authentic Hadith."
    
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
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Clear Chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Assalamu alaikum! How can I assist you with Islamic guidance today?"}
        ]
        st.rerun()

# Add footer
st.markdown("---")
st.markdown("*This application provides general guidance based on Islamic teachings. For specific legal or complex religious matters, please consult with qualified scholars.*") 