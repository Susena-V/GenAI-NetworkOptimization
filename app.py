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

# Streamlit app setup
st.markdown(
    """
    <style>
        .purple-glow {
            font-size: 2rem;
            text-align: center;
            color: #6a1b9a;
            text-shadow: 0 0 15px rgba(106, 27, 154, 0.7), 0 0 30px rgba(106, 27, 154, 0.5);
        }
        .chat-container {
            background-color: #000000;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 20px;
        }
        .user-message {
            font-weight: bold;
        }
        .assistant-message {
            color: #2196f3;
            font-style: italic;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="purple-glow">Network Engineer Assistant Chatbot</h1>', unsafe_allow_html=True)

# Display chat logs dynamically
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I assist you with your network engineering tasks today?"}
    ]

# User input
user_input = st.text_input("Your message:", key="user_input", placeholder="Type your query here...")

if st.button("Send"):
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

# Chat UI
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="chat-container"><p class="user-message">You: {msg["content"]}</p></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="chat-container"><p class="assistant-message">Assistant: {msg["content"]}</p></div>',
            unsafe_allow_html=True,
        )

# Generate PDF
if st.button("Generate PDF"):
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

# Clear chat logs
if st.button("Clear Chat Logs"):
    chat_logs.clear()
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I assist you with your network engineering tasks today?"}
    ]
    st.success("Chat logs cleared!")
