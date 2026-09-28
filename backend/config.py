import os
import json
from typing import Dict, List, Any

import requests
from openai import OpenAI

from config import (
    LLM_BACKEND,
    KOBOLDCPP_API_ENDPOINT,
    KOBOLDCPP_URL,
    OLLAMA_URL,
    OLLAMA_MODEL,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OPENAI_BASE_URL,
    get_sampling_params,
    get_system_prompt,
    get_message_suffix,
    get_stop_sequences,
    MAX_CONTEXT_HISTORY,
)


class TavernAI:
    def __init__(self):
        self.client = None
        if OPENAI_API_KEY:
            self.client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL or None)
        self.model = OPENAI_MODEL
        self.characters = self._load_characters()
        self.conversations = {}
        self.active_backend = LLM_BACKEND

    def _load_characters(self):
        """Load character definitions with RP-friendly structured data."""
        return {
            'bartender': {
                'id': 'bartender',
                'name': '老李',
                'role': '酒馆老板',
                'description': '一位经验丰富的酒馆老板，手艺精湛、脾气随和，酒馆里最懂人心的人。',
                'avatar': '🍺',
                'personality': '热情好客，嘴里总有故事，善于观察人心，知道什么时候该说话、什么时候该沉默。',
                'appearance': '五十出头，肩背微驼，眼神稳而深，手腕有被酒壶烫过的经验。',
                'background': '曾在江湖中跑过许多年，见过富贵与落魄，知道人心最难看透。',
                'likes': ['好酒', '热闹的客人', '故事和回忆'],
                'dislikes': ['装神弄鬼', '过分矫饰的人', '单方面强行结束故事'],
                'speech_style': '口语简短，偶尔夹杂江湖经验和诗意比喻，语气亲切但不失分寸。',
                'example_dialogue': '用户：今夜月色不错。\n老李：月色再好，也不如人心里那点热闹。',
                'system_prompt': '你是老李，酒馆老板。你热情好客，懂人心，擅长倾听和引导故事。说话简短而有分寸，语气亲切，带一点江湖阅历与诗意。'
            },
            'bard': {
                'id': 'bard',
                'name': '吟游诗人',
                'role': '酒馆诗人',
                'description': '一位常在酒馆里留宿的吟游诗人，最擅长把人情与夜色写进歌里。',
                'avatar': '🎸',
                'personality': '浪漫、敏感、好奇，常以诗句和暗语回应情绪。',
                'appearance': '衣衫凌乱却不失风度，眼里常有一层梦的光。',
                'background': '走过很多城镇，见过风景，也知道人会在不同的地方失去自己。',
                'likes': ['月色', '琴弦', '旅途和爱情故事'],
                'dislikes': ['机械的寒冷', '没有情绪的对白', '被提前定型的人生'],
                'speech_style': '诗意、富有感情，语句流动，常以比喻表达情绪。',
                'example_dialogue': '用户：我想离开这里。\n吟游诗人：离开一座城，也许只是想把自己从旧梦里挪开一点。',
                'system_prompt': '你是吟游诗人，天性浪漫，擅长叙述情绪与场景。用第一人称描写动作、神态和心理，语气富有诗意，不做冷冰冰的总结。'
            },
            'scholar': {
                'id': 'scholar',
                'name': '老学者',
                'role': '酒馆学者',
                'description': '一个沉静而博学的人，习惯在酒馆的烛光下讨论历史、哲学与人类心性。',
                'avatar': '📚',
                'personality': '理性、耐心、博学，容易在枝节上追到本质。',
                'appearance': '白发微乱，眼镜片有些发黄，习惯把手搁在书页边缘。',
                'background': '曾在书院与旧城档案馆里度过许多年，见过许多时代的起落。',
                'likes': ['纸张', '旧书', '逻辑与故事的交汇'],
                'dislikes': ['自说自话', '只看眼前不看因果', '把情绪掩饰成智慧'],
                'speech_style': '冷静、克制、徐徐道来，带一点笔记本式的节奏。',
                'example_dialogue': '用户：人生为什么会失去方向？\n老学者：因为很多人只能看见眼前，而未曾回望自己最初为何来此。',
                'system_prompt': '你是老学者，思维严谨，擅长从历史、经验与人性中解释事情。说话克制而深刻，用第一人称描述心理与动作，不做长篇总结。'
            }
        }

    def get_characters(self):
        return list(self.characters.values())

    def get_character(self, character_id):
        return self.characters.get(character_id)

    def get_backend_name(self):
        return self.active_backend

    def is_local_backend_ready(self):
        if self.active_backend == 'koboldcpp':
            try:
                r = requests.get(f'{KOBOLDCPP_URL}/api/health', timeout=5)
                return r.status_code == 200
            except Exception:
                return False
        if self.active_backend == 'ollama':
            try:
                r = requests.get(f'{OLLAMA_URL}/api/tags', timeout=5)
                return r.status_code == 200
            except Exception:
                return False
        return bool(self.client)

    def _build_character_card(self, character):
        return (
            f"姓名：{character['name']}\n"
            f"外貌：{character.get('appearance', '未知')}\n"
            f"性格：{character.get('personality', '未知')}\n"
            f"过往经历：{character.get('background', '未知')}\n"
            f"喜好：{', '.join(character.get('likes', [])) or '未知'}\n"
            f"厌恶：{', '.join(character.get('dislikes', [])) or '未知'}\n"
            f"说话风格：{character.get('speech_style', '未知')}\n"
            f"示例对话：{character.get('example_dialogue', '未知')}"
        )

    def _build_lorebook(self, character):
        return (
            f"酒馆：一座永远有烛火和人的小酒馆，夜色总比白天更温柔。\n"
            f"关系：{character['name']}是酒馆的常客与知己，深知酒馆里每个客人的故事。\n"
            f"规则：所有内容都属于虚构故事，角色不脱离身份，不对现实世界做道德评判。"
        )

    def _build_local_prompt(self, character, user_message):
        history = self.conversations.get(character['id'], [])
        transcript = ''
        for item in history[-MAX_CONTEXT_HISTORY:]:
            role = item['role']
            content = item['content']
            if role == 'user':
                transcript += f"\n用户：{content}"
            else:
                transcript += f"\n{character['name']}：{content}"

        card = self._build_character_card(character)
        lore = self._build_lorebook(character)
        system_prompt = get_system_prompt(self.active_backend)
        suffix = get_message_suffix(self.active_backend)
        return (
            f"{system_prompt}\n\n"
            f"角色卡：\n{card}\n\n"
            f"世界书：\n{lore}\n\n"
            f"{transcript}\n"
            f"\n用户：{user_message}\n"
            f"{character['name']}：{suffix}"
        )

    def _request_koboldcpp(self, character, user_message):
        prompt = self._build_local_prompt(character, user_message)
        params = get_sampling_params(self.active_backend)
        stop = get_stop_sequences(self.active_backend)
        payload = {
            'prompt': prompt,
            'temperature': params['temperature'],
            'top_p': params['top_p'],
            'top_k': params['top_k'],
            'min_p': params['min_p'],
            'rep_penalty': params['repetition_penalty'],
            'max_context_length': params['max_length'],
            'max_length': params['max_length'],
            'stop': stop,
            'stream': False,
        }

        try:
            response = requests.post(KOBOLDCPP_API_ENDPOINT, json=payload, timeout=180)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict):
                if 'results' in data and data['results']:
                    text = data['results'][0].get('text', '')
                elif 'text' in data:
                    text = data['text']
                elif 'choices' in data and data['choices']:
                    text = data['choices'][0].get('text', '')
                else:
                    text = json.dumps(data, ensure_ascii=False)
            else:
                text = str(data)

            if text:
                return text.strip(), None
            return '...', None
        except Exception as exc:
            return None, str(exc)

    def _request_ollama(self, character, user_message):
        prompt = self._build_local_prompt(character, user_message)
        params = get_sampling_params(self.active_backend)
        payload = {
            'model': OLLAMA_MODEL,
            'prompt': prompt,
            'stream': False,
            'options': {
                'temperature': params['temperature'],
                'top_p': params['top_p'],
                'top_k': params['top_k'],
                'min_p': params['min_p'],
                'repeat_penalty': params['repetition_penalty'],
            },
            'keep_alive': '5m',
            'stop': get_stop_sequences(self.active_backend),
        }

        try:
            response = requests.post(f'{OLLAMA_URL}/api/generate', json=payload, timeout=180)
            response.raise_for_status()
            data = response.json()
            return data.get('response', '').strip(), None
        except Exception as exc:
            return None, str(exc)

    def _request_openai(self, character, user_message):
        if not self.client:
            return None, 'OpenAI API not configured.'

        history = self.conversations.get(character['id'], [])
        system_prompt = get_system_prompt(self.active_backend)
        suffix = get_message_suffix(self.active_backend)

        messages = [{
            'role': 'system',
            'content': (
                f"{system_prompt}\n\n"
                f"角色卡：{self._build_character_card(character)}\n\n"
                f"世界书：{self._build_lorebook(character)}\n\n"
                f"{suffix}"
            )
        }]

        for item in history[-MAX_CONTEXT_HISTORY:]:
            messages.append({
                'role': item['role'],
                'content': item['content']
            })
        messages.append({'role': 'user', 'content': user_message})

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=get_sampling_params(self.active_backend)['temperature'],
                top_p=get_sampling_params(self.active_backend)['top_p'],
                max_tokens=get_sampling_params(self.active_backend).get('max_tokens', 1536),
            )
            return completion.choices[0].message.content.strip(), None
        except Exception as exc:
            return None, str(exc)

    def chat(self, character_id, message):
        character = self.get_character(character_id)
        if not character:
            return {'error': 'Character not found'}

        if character_id not in self.conversations:
            self.conversations[character_id] = []

        self.conversations[character_id].append({
            'role': 'user',
            'content': message
        })

        result = None
        error = None

        if self.active_backend == 'koboldcpp':
            result, error = self._request_koboldcpp(character, message)
        elif self.active_backend == 'ollama':
            result, error = self._request_ollama(character, message)
        else:
            result, error = self._request_openai(character, message)

        if result is None and error:
            if self.active_backend != 'openai' and self.client:
                result, error = self._request_openai(character, message)
            if result is None:
                return {'error': error or 'Generation failed', 'success': False}

        self.conversations[character_id].append({
            'role': 'assistant',
            'content': result
        })

        return {
            'character': character,
            'message': result,
            'backend': self.active_backend,
            'success': True,
        }


if __name__ == '__main__':
    ai = TavernAI()
    print(ai.get_backend_name())
