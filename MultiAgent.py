from groq import Groq
import os

# Initialize Groq client
client = Groq()

# Setting up the initial system message
system_message = "You are a network engineer's assistant and you will analyze data given from other sources and answer the user's query."

# Start a loop for continuous user input and chat
while True:
    user_input = input("You: ")  # Prompt the user for input
    
    if user_input.lower() == 'exit':  # Allow the user to exit the chat
        print("Exiting chat...")
        break

    # Make the chat completion API call to Groq with the user input
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input}
        ],
        model="llama3-70b-8192"  # Specify the model you're using
    )

    # Print the assistant's response
    assistant_response = chat_completion.choices[0].message.content
    print(f"Assistant: {assistant_response}")
