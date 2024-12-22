import streamlit as st
from chat_logic import initialize_chat_state, handle_user_input, generate_pdf, clear_chat_logs

# UI Styles
st.markdown(
    """
    <style>
        @keyframes glow {
            0% {
                text-shadow: 0 0 15px rgba(106, 27, 154, 0.7),
                            0 0 30px rgba(106, 27, 154, 0.5);
            }
            50% {
                text-shadow: 0 0 20px rgba(106, 27, 154, 0.9),
                            0 0 40px rgba(106, 27, 154, 0.7),
                            0 0 60px rgba(106, 27, 154, 0.5);
            }
            100% {
                text-shadow: 0 0 15px rgba(106, 27, 154, 0.7),
                            0 0 30px rgba(106, 27, 154, 0.5);
            }
        }

        .purple-glow {
            font-size: 3rem;
            text-align: center;
            color: #6a1b9a;
            animation: glow 2s ease-in-out infinite;
            margin-bottom: 0rem;
        }
        
        /* Chat container styling */
        .chat-container {
            border-radius: 10px;
            padding: 10px 40px;
            margin-bottom: 10px;
            position: relative;
        }
        
        .bgcolor-assist {
            background-color: #000000;
        }
        
        .bgcolor-use {
            background-color: #aa00ff;
        }
        
        /* Message styling */
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
        
        /* Emoji styling */
        .emoji {
            position: absolute;
            font-size: 1.5rem;
            top: 50%;
            transform: translateY(-50%);
        }
        
        .user-emoji {
            right: -35px;
        }
        
        .bot-emoji {
            left: -35px;
        }
        
        /* Input container styling */
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
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .fixed-input-container {
                padding: 0.5rem;
            }
            .purple-glow {
                font-size: 2rem;
            }
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
                f'''<div class="chat-container bgcolor-use">
                    <div class="emoji user-emoji">😸</div>
                    <div class="message-content user-message">{msg["content"]}</div>
                </div>''',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'''<div class="chat-container bgcolor-assist">
                    <div class="emoji bot-emoji">🦄</div>
                    <div class="message-content assistant-message">{msg["content"]}</div>
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