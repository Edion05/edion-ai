import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- INITIAL SETUP ---
# Get your key at aistudio.google.com
genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Edion AI", page_icon="⚡", layout="centered")

# --- EDION UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stChatFloatingInputContainer { background-color: #050505; }
    div[data-testid="stChatMessage"] { background-color: #111111; border-radius: 15px; border: 1px solid #333; }
    .premium-btn { background-color: #FF4B4B; color: white; padding: 10px; border-radius: 10px; text-decoration: none; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE (The Memory) ---
if "chat_session" not in st.session_state:
    # This starts a real conversation thread with history
    st.session_state.chat_session = model.start_chat(history=[])

# --- SIDEBAR (Premium & File Upload) ---
with st.sidebar:
    st.title("Edion AI ⚡")
    is_premium = st.toggle("Unlock Edion Premium")
    
    if not is_premium:
        st.markdown('<a href="https://buy.stripe.com/your_link" class="premium-btn">Go Premium ($5)</a>', unsafe_allow_html=True)
    
    st.divider()
    uploaded_file = st.file_uploader("Upload a file for Edion to analyze", type=['png', 'jpg', 'jpeg', 'pdf'])

# --- CHAT INTERFACE ---
st.title("Edion AI")
st.caption("Powered by Simplified Intelligence")

# Display chat history from the session
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# User Input
if prompt := st.chat_input("Ask Edion anything..."):
    # Show user message
    st.chat_message("user").markdown(prompt)
    
    # Process with File if exists
    content_to_send = [prompt]
    if uploaded_file:
        img = Image.open(uploaded_file)
        content_to_send.append(img)
        st.info("Analyzing file...")

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Edion is thinking..."):
            # If not premium, add a "personality" restriction
            if not is_premium:
                prompt_suffix = " (Note: Provide a helpful but brief summary)."
            else:
                prompt_suffix = " (Note: You are in Premium Mode. Provide deep, expert analysis)."
            
            # This line sends the message AND saves it to history automatically
            response = st.session_state.chat_session.send_message(content_to_send)
            st.markdown(response.text)
