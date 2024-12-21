from flask import Flask, render_template, request, jsonify, send_file
from groq import Groq
from fpdf import FPDF
import os

# Initialize Groq client
client = Groq()

# Initialize Flask app
app = Flask(__name__)

# Create a directory to store generated PDFs
if not os.path.exists('docs'):
    os.makedirs('docs')

# Initialize an empty list to hold chat logs
chat_logs = []

# Setting up the initial system message
system_message = """
You are a network engineer's assistant and you will analyze data given from other sources and answer the user's query.

You must be able to detect anomalies.
You must be able to reallocate resources dynamically.
You must be able to predict future bottleneck points.
You should provide documentation on the network and failures."""

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']

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

    # Log the conversation
    chat_logs.append(f"You: {user_input}")
    chat_logs.append(f"Assistant: {assistant_response}")

    return jsonify({'response': assistant_response})

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
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

    # Return the PDF file for download
    return send_file(pdf_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
