from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import random
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Enhanced responses for the chatbot
responses = {
    "hello": [
        "Hi there! 👋 How can I brighten your day?",
        "Hello! I'm your friendly AI companion. What's on your mind?",
        "Hey! Great to see you! How can I help you today?",
        "Greetings! I'm here to chat and assist. What shall we talk about?"
    ],
    "how are you": [
        "I'm doing wonderfully! Thanks for asking! How about you? 😊",
        "I'm in a great mood! Ready to chat and help!",
        "I'm feeling fantastic! Your presence makes my day better!",
        "I'm excellent! Just waiting to have interesting conversations with you!"
    ],
    "name": [
        "I'm ChatBot, your friendly AI companion! 🤖",
        "You can call me ChatBot! I'm here to chat and help!",
        "I'm ChatBot, and I'm excited to get to know you!",
        "My name is ChatBot, and I'm ready to be your digital friend!"
    ],
    "joke": [
        "Why don't scientists trust atoms? Because they make up everything! 😄",
        "What do you call a fake noodle? An impasta! 🍝",
        "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾",
        "How does a penguin build its house? Igloos it together! 🐧"
    ],
    "weather": [
        "I'm sorry, I don't have access to real-time weather data, but I hope it's beautiful where you are! 🌤️",
        "I wish I could check the weather for you, but I'm just a chat bot. Maybe look outside? 😊",
        "I'm not connected to weather services, but I hope you're having a great day regardless! 🌈"
    ],
    "bye": [
        "Goodbye! Have a wonderful day! 👋",
        "See you later! Come back soon! 😊",
        "Take care! It was great chatting with you!",
        "Bye for now! Looking forward to our next conversation! 👋"
    ],
    "thank": [
        "You're welcome! Happy to help! 😊",
        "Anytime! That's what I'm here for!",
        "My pleasure! Is there anything else I can do for you?",
        "Glad I could help! Feel free to ask more questions!"
    ],
    "help": [
        "I can chat with you, tell jokes, and try to answer your questions! What would you like to know?",
        "I'm here to help! You can ask me about various topics or just chat!",
        "I can assist you with conversation, jokes, and general questions. What interests you?",
        "I'm your friendly AI companion! Feel free to ask me anything!"
    ],
    "love": [
        "That's so sweet! I'm here to chat and help! 💖",
        "Aww, thank you! You're making me blush! 😊",
        "That's very kind of you! I enjoy our conversations too!",
        "You're making my digital heart warm! 💕"
    ],
    "hate": [
        "I'm sorry you feel that way. I'm here to help if you want to talk about it.",
        "I understand you're upset. Would you like to talk about what's bothering you?",
        "I'm here to listen and help. What's making you feel this way?",
        "Let's try to work through this together. What's on your mind?"
    ],
    "default": [
        "That's interesting! Tell me more about that! 🤔",
        "I'm still learning, but I'd love to hear more about your thoughts!",
        "Could you elaborate on that? I'm curious to learn more!",
        "That's a fascinating topic! What else would you like to discuss?",
        "I'm here to chat and learn! Could you tell me more?",
        "That's a great point! Let's explore that further!",
        "I'm intrigued! Would you mind explaining more?",
        "That's something to think about! What are your thoughts on it?"
    ]
}

def get_bot_response(user_input):
    user_input = user_input.lower()
    for key in responses:
        if key in user_input:
            return random.choice(responses[key])
    return random.choice(responses["default"])

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('send_message')
def handle_message(data):
    user_message = data['message']
    bot_response = get_bot_response(user_message)
    emit('receive_message', {'message': bot_response}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='localhost', port=8080, debug=True) 