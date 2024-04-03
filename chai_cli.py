import requests
from summa import summarizer
import os
import logging
from dotenv import load_dotenv

# Loads environment variables from a .env file into the environment
load_dotenv()
API_URL = os.getenv("CHATBOT_API_URL")
API_KEY = os.getenv("CHATBOT_API_KEY")

def save_bot_name(name):
    with open('bot_name.txt', 'w') as file:
        file.write(name)

def load_bot_name(default='Harry Potter'):
    try:
        with open('bot_name.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return default
    

# Configuration and global variables
summarization_ratio = 0.5
bot_memory = ""
chat_history = []
bot_name = load_bot_name()
user_name = "You"


def summarize_conversation(chat_history):
    """
    Summarizes the chat history into a concise memory string using the summa summarizer.

    :param chat_history: List of chat messages between the user and the bot.
    :return: Summarized version of the conversation or an empty string if an error occurs.
    """
    try:
        sentences = [f"{chat['sender']}: {chat['message']}" for chat in chat_history]
        script = "\n".join(sentences)
        summary = summarizer.summarize(script, ratio=summarization_ratio)
        return summary
    except Exception as e:
        logging.error(f"Error summarizing conversation: {e}")
        return ""


def send_message_to_chatbot(user_message):
    """
    Sends a user message to the chatbot API and updates the conversation history and bot memory based on the response.

    :param user_message: The message from the user to the chatbot.
    :return: The chatbot's response message or an error message if the API call fails.
    """
    global bot_memory, chat_history, bot_name, user_name

    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {
        "memory": bot_memory,
        "prompt": user_message,  
        "bot_name": bot_name,
        "user_name": user_name,
        "chat_history": chat_history
        }

    try:
        response = requests.post(API_URL, json=data, headers=headers)
        response.raise_for_status() 
        bot_message = response.json().get('model_output', '')
        chat_history.append({"sender": user_name, "message": user_message})
        chat_history.append({"sender": bot_name, "message": bot_message})
        bot_memory = summarize_conversation(chat_history)
        return bot_message
    
    except requests.exceptions.HTTPError as http_err:
        logging.error(f" HTTP error occurred: {http_err} ")

    except Exception as e:
        logging.error(f" Error sending message to chatbot: {e} ")

    return "I'm currently having issues, please try again later."


def chat_session():
    """
    Initiates a chat session where the user can interact with the chatbot. 
    The session runs in a loop until the user quits.
    """
    global chat_history, bot_name, user_name
    print("_____________________________________________\n")
    print("CHATBOT SESSION STARTED. Type 'quit' to exit.")
    print("_____________________________________________\n")
    print(f"The last bot you chatted with was {bot_name}.")
    user_input = input("Please enter the name of the bot you'd like to chat with, or press enter to continue: ")
    print("_____________________________________________\n")
    if user_input.strip():
        bot_name = user_input
        save_bot_name(bot_name)
   
    while True:
        message = input(f"{user_name}: ")
        if message.lower() in ['quit', 'exit']:
            print("_____________________________________________\n")
            print("EXITING CHAT SESSION.")
            print("_____________________________________________\n")
            break
        response = send_message_to_chatbot(message)
        print(f"{bot_name}:", response)


if __name__ == "__main__":
    chat_session()
