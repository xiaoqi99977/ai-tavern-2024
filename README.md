# 🍺 AI酒馆 (AI Tavern)

一个交互式AI驱动的虚拟酒馆，你可以与各种独特的AI角色聊天。

## 功能特性

- 🤖 多个AI角色，每个都有独特的性格和背景
- 💬 实时对话，支持长期对话历史
- 🎨 美观的Web界面
- 🔌 易于扩展的后端架构
- 🚀 基于OpenAI API

## 项目结构

```
ai-tavern-2024/
├── backend/              # Python Flask 后端
│   ├── app.py           # 主应用文件
│   ├── tavern_ai.py     # AI逻辑和角色定义
│   ├── requirements.txt  # Python依赖
│   └── .env.example     # 环境变量示例
├── frontend/            # 前端页面
│   ├── index.html       # HTML页面
│   ├── styles.css       # 样式文件
│   └── script.js        # JavaScript逻辑
└── README.md           # 项目说明
```

## 快速开始

### 前置要求

- Python 3.8+
- Node.js/npm (可选，用于前端开发)
- OpenAI API Key

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/xiaoqi99977/ai-tavern-2024.git
   cd ai-tavern-2024
   ```

2. **配置后端**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **设置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，添加你的 OpenAI API Key
   ```

4. **运行后端**
   ```bash
   python app.py
   # 后端运行在 http://localhost:5000
   ```

5. **运行前端**
   - 在浏览器中打开 `frontend/index.html`
   - 或使用 Live Server 等工具
   - 访问 `http://localhost:8000` (如果使用开发服务器)

## API 端点

- `GET /api/health` - 健康检查
- `GET /api/characters` - 获取所有角色
- `GET /api/character/<id>` - 获取特定角色
- `POST /api/chat` - 发送消息并获取回复

### 聊天请求示例

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "character_id": "bartender",
    "message": "你好！"
  }'
```

## 已有角色

1. **老李 (Bartender)** 🍺
   - 经验丰富的酒馆老板
   - 知识渊博，善于倾听
   - 热情好客，爱讲故事

2. **吟游诗人 (Bard)** 🎸
   - 浪漫的酒馆诗人
   - 擅长讲述冒险故事
   - 幽默风趣，富有想象力

3. **老学者 (Scholar)** 📚
   - 博学的学者
   - 对历史和知识充满热情
   - 严谨认真，喜欢讨论哲学

## 自定义添加角色

在 `backend/tavern_ai.py` 中修改 `_load_characters()` 方法：

```python
'new_character': {
    'id': 'new_character',
    'name': '角色名称',
    'role': '角色职位',
    'description': '角色描述',
    'avatar': '😀',
    'personality': '性格描述',
    'system_prompt': 'Character system prompt for OpenAI API...'
}
```

## 环境变量

- `OPENAI_API_KEY` - OpenAI API密钥（必需）
- `FLASK_ENV` - Flask环境（development/production）

## 技术栈

### 后端
- Python 3.8+
- Flask - Web框架
- Flask-CORS - 跨域资源共享
- OpenAI - AI API

### 前端
- HTML5
- CSS3
- Vanilla JavaScript

## 未来功能计划

- [ ] 用户认证系统
- [ ] 持久化对话历史（数据库）
- [ ] 角色自定义系统
- [ ] 多语言支持
- [ ] 移动应用版本
- [ ] 实时WebSocket通信
- [ ] 角色语音合成
- [ ] 高级对话分析

## 故障排除

### 后端无法连接
- 确保后端正在 localhost:5000 运行
- 检查 CORS 配置
- 查看浏览器控制台的错误信息

### OpenAI API 错误
- 验证 API Key 是否正确
- 检查 API 配额和使用情况
- 确保网络连接正常

### 消息发送失败
- 检查浏览器网络选项卡
- 验证请求格式
- 查看后端日志

## 许可证

MIT License

## 贡献

欢迎提交 Issues 和 Pull Requests！

## 联系方式

- GitHub: [@xiaoqi99977](https://github.com/xiaoqi99977)
- 项目仓库: [ai-tavern-2024](https://github.com/xiaoqi99977/ai-tavern-2024)
