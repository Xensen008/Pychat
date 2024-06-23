#personality based chatbot

import google.generativeai as genai
import os
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

conversation_history = []

def chat_with_ai(user_input):
    global conversation_history

    if user_input.lower() == "reset conversation":
        conversation_history = []
        return "Conversation reset. How can I assist you?"
        
    # Proceed with generating a response for all queries
    conversation_history.append(f"You: {user_input}")
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    full_conversation = "\n".join(conversation_history)
    response = model.generate_content(full_conversation + f"\nAI (as a Personal assistant):")
    formatted_response = response.text.replace('*', '')
    conversation_history.append(f"AI: {formatted_response}")
        
    # Format the conversation history for display
    formatted_conversation_history = "\n".join([f"> {line}" if line.startswith("You:") else f"- {line}" for line in conversation_history])
    return formatted_conversation_history

# Setup Gradio interface
interface = gr.Interface(
    fn=chat_with_ai,
    inputs=gr.Textbox(lines=2, placeholder="Enter your message here...", label="Your Message"),
    outputs=gr.Textbox(label="Conversation", lines=20, placeholder="Conversation will appear here..."),
    title="Personal Chat Assistant",
    description="I am a Personal assistant here to help with your All type queries. Let's chat!",
    examples=[["Write an eassy on read dangers?"], ["Explain compiler interpreter."]],
    css="""
        .output_text { color: black; font-family: Arial; }
        .input_text { display: flex; flex-direction: row; align-items: center; }
        .input_text textarea { flex-grow: 1; }
        .input_text button { width: 100px; }
    """
)

# Launch the interface with sharing enabled
interface.launch()