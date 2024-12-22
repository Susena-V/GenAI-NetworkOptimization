from fpdf import FPDF
from groq import Groq
import os

# Create Groq client
client = Groq()

# Create a directory for storing generated PDFs
if not os.path.exists("docs"):
    os.makedirs("docs")

# Define system message
SYSTEM_MESSAGE = """
You are a network engineer's assistant and you will analyze data given from other sources and answer the user's query.

You must be able to detect anomalies.
You must be able to reallocate resources dynamically.
You must be able to predict future bottleneck points.
You should provide documentation on the network and failures.
"""

def initialize_chat_state(session_state):
    """Initialize chat state in Streamlit session."""
    if "messages" not in session_state:
        session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your network assistant buddy. How can I assist you with your network engineering tasks today?"}
        ]

def handle_user_input(user_input, session_state):
    """Process user input and update session state."""
    if user_input:
        session_state.messages.append({"role": "user", "content": user_input})
        chat_response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": user_input}
            ],
            model="llama3-70b-8192"  # Specify the model you're using
        )
        assistant_response = chat_response.choices[0].message.content
        session_state.messages.append({"role": "assistant", "content": assistant_response})

def generate_pdf(session_state):
    """Generate PDF from chat logs."""
    if session_state.messages:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for msg in session_state.messages:
            role = "You" if msg["role"] == "user" else "Assistant"
            pdf.multi_cell(0, 10, f"{role}: {msg['content']}")

        pdf_filename = "docs/chat_log.pdf"
        pdf.output(pdf_filename)
        return pdf_filename
    return None

def clear_chat_logs(session_state):
    """Clear chat logs and reset to initial state."""
    session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I assist you with your network engineering tasks today?"}
    ]
