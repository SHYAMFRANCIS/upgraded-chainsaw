import os
import google.generativeai as genai
from datetime import datetime
import json
import logging

api_key = "AIzaSyDYDnb5_fZNK_IXg3Uw-GynalxsCrkqlog"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
 
try:
    GEMINI_API_KEY = api_key
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API configured successfully.")
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {str(e)}")
    exit(1)

# Initialize conversation history
HISTORY_FILE = "conversation_history.json"
conversation_history = []

def load_history():
    """Load conversation history from a JSON file."""
    global conversation_history
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                conversation_history = json.load(f)
            logger.info("Conversation history loaded.")
        else:
            logger.info("No conversation history found. Starting fresh.")
    except Exception as e:
        logger.error(f"Error loading history: {str(e)}")

def save_history():
    """Save conversation history to a JSON file."""
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(conversation_history, f, indent=2)
        logger.info("Conversation history saved.")
    except Exception as e:
        logger.error(f"Error saving history: {str(e)}")

def initialize_model():
    """Initialize the Gemini model."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("Gemini model initialized.")
        return model
    except Exception as e:
        logger.error(f"Error initializing model: {str(e)}")
        return None

def generate_response(model, user_input):
    """Generate a response using the Gemini model."""
    try:
        # Prepare context with conversation history
        context = (
            "You are a Doubt Resolution Bot specialized in Google Gemini API key issues. "
            "Provide clear, accurate, and concise answers to user queries about Gemini API key setup, usage, troubleshooting, and best practices. "
            "Use technical details when necessary but keep explanations beginner-friendly. "
            "Here is the conversation history for context:\n"
        )
        for entry in conversation_history[-5:]:  # Limit to last 5 exchanges
            context += f"User: {entry['user']}\nBot: {entry['bot']}\n"

        context += f"User: {user_input}\nBot: "
        
        # Generate response
        response = model.generate_content(context)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return "Sorry, I encountered an error. Please try again or rephrase your question."

def main():
    """Main function to run the Doubt Resolution Bot."""
    load_history()
    model = initialize_model()
    
    if not model:
        logger.error("Exiting due to model initialization failure.")
        return

    print("Welcome to the Gemini API Key Doubt Resolution Bot!")
    print("Ask your questions about Gemini API key setup, usage, or troubleshooting.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            save_history()
            break

        if not user_input.strip():
            print("Please enter a valid question.")
            continue

        # Generate and display response
        response = generate_response(model, user_input)
        print(f"Bot: {response}\n")

        # Update conversation history
        conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "bot": response
        })

        # Save history after each interaction
        save_history()

if __name__ == "__main__":
    main()