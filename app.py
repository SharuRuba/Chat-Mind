from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import random
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Simple responses for the chatbot
responses = {
    "hello": ["Hi there! 👋", "Hello! How can I help you today?", "Hey! Nice to meet you!"],
    "how are you": ["I'm doing great, thanks for asking! 😊", "I'm wonderful! How about you?"],
    "bye": ["Goodbye! 👋", "See you later!", "Take care!"],
    "default": ["I'm not sure I understand. Could you rephrase that?", 
                "Interesting! Tell me more about that.",
                "I'm still learning. Could you explain that differently?"]
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