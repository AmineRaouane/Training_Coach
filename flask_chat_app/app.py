from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ChatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.Column(db.Text, nullable=False)  # Storing as JSON string

@app.route('/append_interaction/<int:chat_id>', methods=['POST'])
def append_interaction(chat_id):
    data = request.get_json()

    chat = ChatSession.query.get_or_404(chat_id)
    current_messages = json.loads(chat.messages)
    current_messages.append(data)

    chat.messages = json.dumps(current_messages)
    db.session.commit()

    return jsonify({'message': 'Interaction appended successfully'}), 200

@app.route('/add_chat', methods=['POST'])
def add_chat():
    data = request.get_json()
    title = data.get('title', 'new_chat')
    messages = data.get('messages', [])

    new_chat = ChatSession(
        title=title,
        messages=json.dumps(messages)  # type:ignore
    )
    db.session.add(new_chat)
    db.session.commit()
    return jsonify({'id': new_chat.id, 'message': 'Chat session added successfully'}), 201

@app.route('/get_chats', methods=['GET'])
def get_chats():
    chats = ChatSession.query.order_by(ChatSession.date.desc()).all()
    return jsonify([{
        'id': chat.id,
        'title': chat.title,
        'date': chat.date.isoformat(),
        'messages': json.loads(chat.messages)  # Convert JSON string back to list
    } for chat in chats])

@app.route('/get_chat/<int:chat_id>', methods=['GET'])
def get_chat(chat_id):
    chat = ChatSession.query.get_or_404(chat_id)
    return jsonify({
        'id': chat.id,
        'title': chat.title,
        'date': chat.date.isoformat(),
        'messages': json.loads(chat.messages)
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
