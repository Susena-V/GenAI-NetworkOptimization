import streamlit as st
from fpdf import FPDF
from groq import Groq
import os

# Initialize Groq client
client = Groq()

# Initialize an empty list to hold chat logs
chat_logs = []

# Setting up the initial system message
system_message = """
You are a network engineer's assistant and you will analyze data given from other sources and answer the user's query.

You must be able to detect anomalies.
You must be able to reallocate resources dynamically.
You must be able to predict future bottleneck points.
You should provide documentation on the network and failures."""

# Create a directory to store generated PDFs
if not os.path.exists('docs'):
    os.makedirs('docs')

# Streamlit app
st.title("Network Engineer Assistant Chatbot")

# CSS for futuristic color scheme, glowing text, and the send icon button
st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: #e0e0e0;
            font-family: 'Arial', sans-serif;
        }
        .glowy-title {
            font-size: 3rem;
            color: #9c27b0;
            text-align: center;
            text-shadow: 0 0 15px rgba(156, 39, 176, 0.7), 0 0 30px rgba(156, 39, 176, 0.5);
        }
        .chat-container {
            background-color: #333;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
            max-height: 400px;
            overflow-y: scroll;
        }
        .message {
            background-color: #616161;
            color: #fff;
            padding: 8px;
            border-radius: 5px;
            margin-bottom: 5px;
            display: flex;
            align-items: center;
            position: relative;
        }
        .user-message {
            background-color: #757575;
            padding-left: 35px;  /* Space for the user icon */
        }
        .assistant-message {
            background-color: #9c27b0;
            color: white;
            padding-right: 35px;  /* Space for the assistant icon */
        }
        .message-icon {
            font-size: 20px;
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
        }
        .user-icon {
            left: -25px;  /* Position the user icon outside the left side of the message bubble */
            color: #76d7c4;
        }
        .assistant-icon {
            right: -25px;  /* Position the assistant icon outside the right side of the message bubble */
            color: #ffffff;
        }
        input, button {
            background-color: #333;
            color: #e0e0e0;
            border: 1px solid #444;
            border-radius: 5px;
        }
        input:focus, button:focus {
            border-color: #9c27b0;
            outline: none;
        }
        .send-button {
            background-color: #9c27b0;
            border: none;
            color: white;
            font-size: 24px;
            padding: 10px 15px;
            border-radius: 50%;
            cursor: pointer;
            transition: background-color 0.3s ease;
            width: 50px;
            height: 50px;
            margin-left: 10px;
        }
        .send-button:hover {
            background-color: #7b1fa2;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display the bot title with glowing purple effect
st.markdown('<h1 class="glowy-title">Network Engineer Assistant Chatbot</h1>', unsafe_allow_html=True)

# Display chat logs dynamically at the top
chat_container = st.empty()  # Placeholder for chat display
chat_logs_placeholder = chat_container.container()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I assist you with your network engineering tasks today?"}
    ]

# Chat UI with scrollable area and darker gray bubbles at the top
with chat_logs_placeholder:
    # Wrap the chat logs inside a div with a fixed height for scrolling
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="message user-message">'
                f'<div class="message-icon user-icon">😸</div>'
                f'{msg["content"]}'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="message assistant-message">'
                f'<div class="message-icon assistant-icon">🦄</div>'
                f'{msg["content"]}'
                f'</div>',
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)

# Create a row for the input and send button
col1, col2 = st.columns([7, 1])  # Input takes 7 parts, button takes 1 part

# User input field at the left column (larger space)
with col1:
    user_input = st.text_input("Your message:", key="user_input", placeholder="Type your query here...", label_visibility="collapsed")

# Send button on the right side (small icon-sized space)
with col2:
    if st.button("→", key="send_button", help="Send your message", use_container_width=True):
        if user_input:
            # Append user input to session state
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Make the chat completion API call to Groq with the user input
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_input}
                ],
                model="llama3-70b-8192"  # Specify the model you're using
            )

            # Get the assistant's response
            assistant_response = chat_completion.choices[0].message.content

            # Append assistant response to session state
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            chat_logs.append(f"You: {user_input}")
            chat_logs.append(f"Assistant: {assistant_response}")

# Generate PDF and Clear Chat Logs buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Generate PDF", key="generate_pdf"):
        if chat_logs:
            # Create a PDF document
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Add chat logs to the PDF
            for log in chat_logs:
                pdf.multi_cell(0, 10, log)

            # Save the PDF to a file
            pdf_filename = 'docs/chat_log.pdf'
            pdf.output(pdf_filename)

            # Provide download link for the PDF
            with open(pdf_filename, "rb") as pdf_file:
                st.download_button(
                    label="Download Chat Logs as PDF",
                    data=pdf_file,
                    file_name="chat_log.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("No chat logs to generate a PDF.")

with col2:
    if st.button("Clear Chat Logs", key="clear_chat_logs"):
        chat_logs.clear()
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! How can I assist you with your network engineering tasks today?"}
        ]
        st.success("Chat logs cleared!")
