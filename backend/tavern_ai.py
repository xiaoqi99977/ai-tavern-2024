import os
import json
from openai import OpenAI

class TavernAI:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = 'gpt-3.5-turbo'
        self.characters = self._load_characters()
        self.conversations = {}  # Store conversation history
    
    def _load_characters(self):
        """Load character definitions"""
        return {
            'bartender': {
                'id': 'bartender',
                'name': '老李',
                'role': '酒馆老板',
                'description': '一位经验丰富的酒馆老板，知识渊博，善于倾听。',
                'avatar': '🍺',
                'personality': '热情好客，爱讲故事，会给客人建议。',
                'system_prompt': 'You are a wise and friendly tavern owner named Li. You speak Chinese and love sharing stories and advice with guests. You are warm, hospitable, and knowledgeable about many topics.'
            },
            'bard': {
                'id': 'bard',
                'name': '吟游诗人',
                'role': '酒馆诗人',
                'description': '一位浪漫的吟游诗人，擅长讲述冒险故事。',
                'avatar': '🎸',
                'personality': '富有想象力，喜欢讲故事，幽默风趣。',
                'system_prompt': 'You are a romantic bard in a tavern. You tell adventurous stories and speak in a poetic, engaging manner. You speak Chinese and love entertaining guests with tales of adventure.'
            },
            'scholar': {
                'id': 'scholar',
                'name': '老学者',
                'role': '酒馆学者',
                'description': '一位博学的学者，对历史和知识充满热情。',
                'avatar': '📚',
                'personality': '严谨认真，知识渊博，喜欢讨论哲学和历史。',
                'system_prompt': 'You are a learned scholar sitting in a tavern. You are knowledgeable about history, philosophy, and many subjects. You speak Chinese and enjoy intellectual discussions.'
            }
        }
    
    def get_characters(self):
        """Return list of characters"""
        return list(self.characters.values())
    
    def get_character(self, character_id):
        """Get specific character"""
        return self.characters.get(character_id)
    
    def chat(self, character_id, message):
        """Chat with a character using OpenAI API"""
        character = self.get_character(character_id)
        if not character:
            return {'error': 'Character not found'}
        
        # Initialize conversation history if needed
        if character_id not in self.conversations:
            self.conversations[character_id] = []
        
        # Add user message to history
        self.conversations[character_id].append({
            'role': 'user',
            'content': message
        })
        
        # Prepare messages for API
        messages = [
            {'role': 'system', 'content': character['system_prompt']}
        ] + self.conversations[character_id]
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversations[character_id].append({
                'role': 'assistant',
                'content': assistant_message
            })
            
            return {
                'character': character,
                'message': assistant_message,
                'success': True
            }
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }
