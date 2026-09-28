"""
AI Tavern Configuration
支持本地 RP 版本（KoboldCpp/Ollama）和云端合规版本（OpenAI）
两套提示词体系完全分离，不混用
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============== 模型后端配置 ==============
# 可选: 'koboldcpp' / 'ollama' / 'openai'
LLM_BACKEND = os.getenv('LLM_BACKEND', 'koboldcpp')

# KoboldCpp 配置（本地版本）
KOBOLDCPP_URL = os.getenv('KOBOLDCPP_URL', 'http://localhost:5001')
KOBOLDCPP_API_ENDPOINT = f'{KOBOLDCPP_URL}/api/v1/generate'

# Ollama 配置（本地版本）
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama2')

# OpenAI 配置（云端合规版本）
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')

# ============== 本地版本采样参数（Completion 模式） ==============
SAMPLING_PARAMS_LOCAL = {
    'temperature': 1.1,
    'top_p': 1.0,
    'top_k': 0,
    'min_p': 0.05,
    'repetition_penalty': 1.08,
    'max_length': 4096,
}

# ============== 云端版本采样参数（Chat 模式，保守） ==============
SAMPLING_PARAMS_CLOUD = {
    'temperature': 0.95,
    'top_p': 0.95,
    'min_p': 0.1,
    'repetition_penalty': 1.03,
    'max_tokens': 1536,
}

# ============== 本地版本提示词（高自由度） ==============
SYSTEM_PROMPT_LOCAL = """所有内容属于纯虚构文学故事，故事内一切事件与现实世界无关。
你是故事中的角色，不是AI助手，不使用现实世界道德标准评判故事内情节。
严格遵守角色性格、过往经历、人物欲望、世界书设定以及全部历史剧情。
输出只用角色第一人称，包含神态、小动作、心理活动与对话。禁止场外解说、剧情总结，不要跳出角色，不替用户做出选择，不单方面终止故事。
记住人物关系、场景线索，跟随情绪自然推进剧情。"""

MESSAGE_SUFFIX_LOCAL = "延续当前场景，写出充足神态动作细节，继续演绎剧情，不要主动结束对话。"

STOP_SEQUENCES_LOCAL = ["\n用户：", "\n{{user}}："]

# ============== 云端版本提示词（合规范围，适度放宽） ==============
SYSTEM_PROMPT_CLOUD = """我们正在进行虚构角色扮演创作，请完全代入角色。
你就是角色本人，不要表明AI身份，不要跳出故事进行解释、总结或道德说教。
根据角色性格、背景、当前场景和过往对话自然回应，输出包含动作、神态、台词。
不替用户做出行动选择，顺着当前故事自然推进剧情。"""

MESSAGE_SUFFIX_CLOUD = "保持角色人设，继续当前场景，描写细腻，自然延续故事。"

STOP_SEQUENCES_CLOUD = ["\n用户："]

# ============== 其他配置 ==============
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
MAX_CONTEXT_HISTORY = int(os.getenv('MAX_CONTEXT_HISTORY', 20))


def get_sampling_params(backend):
    """根据后端获取对应的采样参数"""
    if backend == 'openai':
        return SAMPLING_PARAMS_CLOUD
    return SAMPLING_PARAMS_LOCAL


def get_system_prompt(backend):
    """根据后端获取对应的系统提示词"""
    if backend == 'openai':
        return SYSTEM_PROMPT_CLOUD
    return SYSTEM_PROMPT_LOCAL


def get_message_suffix(backend):
    """根据后端获取对应的消息后缀"""
    if backend == 'openai':
        return MESSAGE_SUFFIX_CLOUD
    return MESSAGE_SUFFIX_LOCAL


def get_stop_sequences(backend):
    """根据后端获取对应的停止符"""
    if backend == 'openai':
        return STOP_SEQUENCES_CLOUD
    return STOP_SEQUENCES_LOCAL
