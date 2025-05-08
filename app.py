from flask import Flask, request, jsonify, render_template
from nlp_bot import get_response  # Import the NLP model
import sqlite3
from sentence_transformers import SentenceTransformer, util  # Import necessary modules

app = Flask(__name__)

# Function to log chat history into the database
def log_chat(user_message, bot_reply):
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_reply TEXT NOT NULL
        )
    """)
    c.execute("INSERT INTO chat_history (user_message, bot_reply) VALUES (?, ?)", (user_message, bot_reply))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']  # Get the user's input
    reply = get_response(user_input)  # Use the NLP model to generate a response
    log_chat(user_input, reply)  # Log the chat into the database
    return jsonify({'reply': reply})  # Return the response as JSON

@app.route('/history', methods=['GET'])
def get_history():
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute("SELECT user_message, bot_reply FROM chat_history")
    history = c.fetchall()
    conn.close()
    return jsonify({'history': history})

if __name__ == '__main__':
    app.run(debug=True)





