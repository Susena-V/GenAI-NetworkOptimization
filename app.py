from flask import Flask, render_template, request, jsonify
from groq import Groq

# Initialize Groq client
client = Groq()

# Initialize Flask app
app = Flask(__name__)

# Setting up the initial system message
system_message = """
You are a network engineer's assistant and you will analyze data given from other sources and answer the user's query.

You must be able to detect anomalies.
You must be able to reallocate resources dynamically.
You must be able to predict future bottleneck points.
You should provide documentation on the network and failures."""

@app.route('/')
def home():
    return render_template('index.html')

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

    return jsonify({'response': assistant_response})

if __name__ == '__main__':
    app.run(debug=True)
