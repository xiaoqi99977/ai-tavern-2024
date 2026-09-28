from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from tavern_ai import TavernAI

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize AI Tavern
tavern_ai = TavernAI()

@app.route('/api/characters', methods=['GET'])
def get_characters():
    """Get all available characters in the tavern"""
    characters = tavern_ai.get_characters()
    return jsonify(characters)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Send a message to a character and get response"""
    data = request.json
    character_id = data.get('character_id')
    message = data.get('message')
    
    if not character_id or not message:
        return jsonify({'error': 'Missing character_id or message'}), 400
    
    response = tavern_ai.chat(character_id, message)
    return jsonify(response)

@app.route('/api/character/<character_id>', methods=['GET'])
def get_character(character_id):
    """Get character details"""
    character = tavern_ai.get_character(character_id)
    if not character:
        return jsonify({'error': 'Character not found'}), 404
    return jsonify(character)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
