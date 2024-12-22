import streamlit as st
from chat_logic import initialize_chat_state, handle_user_input, generate_pdf, clear_chat_logs

# UI Styles
st.markdown(
    """
    <style>
        /* Input field styling */
        .stTextInput input {
            border: 2px solid #6a1b9a;
            border-radius: 6px;
            padding: 8px 12px;
            transition: all 0.3s ease;
        }
        
        .stTextInput input:hover {
            border-color: #9c27b0;
        }
        
        .stTextInput input:focus {
            border-color: #6a1b9a;
            box-shadow: 0 0 8px rgba(106, 27, 154, 0.4);
            outline: none;
        }
        
        /* Button styling */
        .stButton button {
            background-color: transparent;
            border: 2px solid #6a1b9a;
            border-radius: 6px;
            color: #6a1b9a;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background-color: rgba(106, 27, 154, 0.1);
            transform: translateY(-2px);
        }
        
        .stButton button:active {
            transform: translateY(0);
            background-color: rgba(106, 27, 154, 0.2);
        }
        
        .stButton button:focus {
            box-shadow: 0 0 0 2px rgba(106, 27, 154, 0.3);
            outline: none;
        }
        
        
        /* Clear button specific */
        .clear-button button:hover {
            background-color: rgba(106, 27, 154, 0.1) !important;
            border-radius: 4px;
        }
        .purple-glow {
            font-size: 2rem;
            text-align: center;
            color: #6a1b9a;
            text-shadow: 0 0 15px rgba(106, 27, 154, 0.7), 0 0 30px rgba(106, 27, 154, 0.5);
            margin-bottom: 2rem;
        }
        .chat-container {
            background-color: #000000;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .user-message {
            font-weight: bold;
        }
        .assistant-message {
            color: #ffffff;
        }
        .fixed-input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: white;
            padding: 1rem;
            border-top: 1px solid #ddd;
            display: flex;
            gap: 10px;
            align-items: center;
            z-index: 100;
        }
        .main-content {
            margin-bottom: 100px;
        }
        .send-button {
            border: none;
            background: none;
            color: #6a1b9a;
            font-size: 24px;
            padding: 0 10px;
            cursor: pointer;
        }
        .stButton button {
            background: none;
            border: none;
            color: #6a1b9a;
        }
        .clear-button {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 101;
        }
        @media (max-width: 768px) {
            .fixed-input-container {
                padding: 0.5rem;
            }
            .purple-glow {
                font-size: 1.5rem;
            }
        }
        
          .chat-container {
            background-color: #000000;
            border-radius: 10px;
            padding: 10px 40px;
            margin-bottom: 10px;
            position: relative;
        }
        
        .emoji {
            position: absolute;
            font-size: 1.5rem;
            top: 50%;
            transform: translateY(-50%);
        }
        
        .user-emoji {
            right: -30px;
        }
        
        .bot-emoji {
            left: -30px;
        }
        
        .message-content {
            width: 100%;
        }
        
        
        .user-message {
            font-weight: bold;
            padding-left: 30px;
        }
        
        
        .assistant-message {
            color: #ffffff;
            padding-right: 30px;
        }
        
        .action-buttons {
    position: fixed;
    top: 10px;
    right: 10px;
    z-index: 101;
    display: flex;
    gap: 10px;
}

.download-button button {
    background-color: #6a1b9a !important;
    color: white !important;
}

.loading-spinner {
    text-align: center;
    color: #6a1b9a;
    margin: 20px 0;
}
        
     
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.markdown('<h1 class="purple-glow">Network Engineer Assistant Chatbot</h1>', unsafe_allow_html=True)

# Clear Button


# Initialize chat state
initialize_chat_state(st.session_state)

# Main content with messages

with st.container():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'''<div class="chat-container">
                    <div class="emoji user-emoji">😸</div>
                    <div class="message-content user-message">You: {msg["content"]}</div>
                </div>''',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'''<div class="chat-container">
                    <div class="emoji bot-emoji">🦄</div>
                    <div class="message-content assistant-message">Assistant: {msg["content"]}</div>
                </div>''',
                unsafe_allow_html=True,
            )
def submit_message():
    if st.session_state.user_input:
        user_message = st.session_state.user_input
        try:
            with st.spinner('🤔 Thinking...'):
                handle_user_input(user_message, st.session_state)
            st.session_state.user_input = ""
        except Exception as e:
            st.error(f"Sorry, something went wrong: {str(e)}")

# Input container
st.markdown('<div class="fixed-input-container">', unsafe_allow_html=True)
col1, col2 = st.columns([8,1])
with col1:
    user_input = st.text_input(
        "", 
        key="user_input",
        placeholder="Type your query here...",
        label_visibility="collapsed",
        on_change=submit_message
    )
with col2:
    st.button("➤", on_click=submit_message)
st.markdown('</div>', unsafe_allow_html=True)