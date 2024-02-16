from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, disconnect
import json
from explain_terms_chat import ExplainTermsChat

from main_chat import MainChat
from pydantic import BaseModel

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:8000",
            "http://127.0.0.1:8000",
            "http://127.0.0.1:8001",
            "http://127.0.0.1:5000",
            "http://127.0.0.1:5001",
            "http://localhost:8001",
            "http://localhost:8081",
            "http://localhost:8080",
        ]
    }
})
socketio = SocketIO(app, cors_allowed_origins="*")

chat_main = MainChat()

class Message(BaseModel):
    message: str

connected_users = []

@socketio.on('connect')
def handle_connect():
    if request.sid not in connected_users:
        connected_users.append(request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in connected_users:
        connected_users.remove(request.sid)

def broadcast(data):
    for user_sid in connected_users:
        socketio.emit('update', data, to=user_sid)

def broadcast_withoutloading(data):
    for user_sid in connected_users:
        socketio.emit('update_withoutloading', data, to=user_sid)

@app.route('/messages', methods=['POST'])
def add_message():
    message_data = request.json
    response = chat_main.chat(message_data['message'])
    broadcast("update")  # Notify clients to fetch updates
    
    return jsonify({"status": "Message added successfully", "response": response})

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = chat_main.get_conversation_history()[1:]
    return jsonify({"status": "Messages retrieved successfully", "data": messages})

## second
chat_instance = ExplainTermsChat()
@app.route("/termsexplained", methods=["GET"])
def get_termsexplained():
    try:
        print("asking for terms explained")
        data = chat_instance.generate_and_get_explained_list()
        broadcast_withoutloading("update_withoutloading")  # Notify clients to fetch updates
        return jsonify({"status": "Terms Explained retrieved successfully", "data": data})
    except Exception as e:
        response = jsonify({"status": "error", "detail": str(e)})
        response.status_code = 500
        return response
    
@app.route("/termsexplainedwithoutloading", methods=["GET"])    
def get_termsexplained_withoutloading():
    try:
        print("asking for terms explained without loading")
        data = chat_instance.get_explained_list()
        return jsonify({"status": "Terms Explained retrieved successfully", "data": data})
    except Exception as e:
        response = jsonify({"status": "error", "detail": str(e)})
        response.status_code = 500
        return response

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
