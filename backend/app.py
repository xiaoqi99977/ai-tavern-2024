# 🍺 AI酒馆 (AI Tavern)

一个同时支持本地角色扮演模型与云端备用 API 的虚构酒馆聊天应用。

## 设计目标

- 本地优先：KoboldCpp / Ollama + GGUF 模型
- 外部 API 兜底：OpenAI 兼容接口
- 统一 `/api/chat` 接口，前端不需要关心后端类型
- 支持本地高自由度 RP 提示词与云端合规叙事提示词双模式
- 角色卡和世界书规范化，适合长对话剧本推进

## 本地模式推荐

### 1. 安装 KoboldCpp

- 下载地址：<https://github.com/LostRuins/koboldcpp/releases/latest>
- 运行本地服务，默认地址：`http://localhost:5001`
- 加载一个 GGUF 模型

### 2. 安装 Ollama（可选）

- 安装地址：<https://ollama.com>
- 启动：`ollama serve`
- 拉取模型：`ollama pull llama2`
- 默认地址：`http://localhost:11434`

## 快速开始

### 后端

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

### 配置 `.env`

```env
LLM_BACKEND=koboldcpp
KOBOLDCPP_URL=http://localhost:5001
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama2
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 本地模式参数

- Temperature: 1.1
- Min-P: 0.05
- Top-P: 1.0
- Top-K: 0
- Repetition Penalty: 1.08
- Max Length: 4096
- Stop: ["\n用户：", "\n{{user}}："]

### 云端模式参数

- Temperature: 0.95
- Min-P: 0.1
- Top-P: 0.95
- Repetition Penalty: 1.03
- Max Tokens: 1536
- Stop: ["\n用户："]

## 角色卡模板

```text
【姓名】苏晚卿
【性别】女
【身份】江南烟雨楼琴师，身世神秘
【外貌】青衣长裙，腰系银流苏，眉眼清冷，笑时眼下有一颗泪痣，长发半挽，常携古琴。
【性格】外表疏离，内心敏感，善于察言观色，言语含蓄，习惯借琴声抒发情绪。
【背景】出身江南旧族，家族败落后隐居烟雨楼，只在夜间抚琴，很少有人知晓她的过往。
【喜好】雨夜、琴声、旧书、白梅
【厌恶】虚伪权贵、背叛、受人摆布
【口头禅】“公子，琴声随心，人亦随心。”
```

## 前端界面建议

### SillyTavern 相关配置

- 全局 CSS：可直接使用 AI 风月磨砂玻璃布局
- Character Expressions：每个角色独立表情图集
- Background Changer：角色独立背景可选
- API 预设：分成两份：`本地_最高自由度` 与 `云端_适度叙事`

## 目录结构

```text
ai-tavern-2024/
├── backend/
│   ├── app.py
│   ├── tavern_ai.py
│   ├── config.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── README.md
└── .gitignore
```

## 说明

- 本地版本建议使用 Completion 模式，关闭 Instruct 模式。
- 云端版本仅支持在合规范围内进行正常虚构创作，不可尝试绕过安全机制。
- 两套提示词和参数必须分离配置，不混用。

## 未来增强

- 更细化的世界书管理
- 角色专属背景与立绘切换
- 可视化配置面板
- 本地模型状态检测
- 多角色共享剧情上下文

## 许可证

MIT License
