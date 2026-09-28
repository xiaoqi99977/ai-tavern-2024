const API_BASE_URL = 'http://localhost:5000/api';

let currentCharacterId = null;
let currentScene = 'tavern';
let currentExpression = 'normal';
const characters = {};
const conversations = {};
const characterHistory = {};

/* ============ 初始化 ============ */
async function init() {
    await loadBackendStatus();
    await loadCharacters();
    setupEventListeners();
}

/* ============ 后端状态 ============ */
async function loadBackendStatus() {
    const statusEl = document.getElementById('backend-status');
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        if (data && data.status === 'ok') {
            statusEl.textContent = '在线';
            statusEl.classList.remove('status-offline');
            statusEl.classList.add('status-online');
        } else throw new Error('Backend offline');
    } catch (error) {
        statusEl.textContent = '离线';
        statusEl.classList.remove('status-online');
        statusEl.classList.add('status-offline');
    }
}

/* ============ 加载角色 ============ */
async function loadCharacters() {
    try {
        const response = await fetch(`${API_BASE_URL}/characters`);
        const data = await response.json();

        data.forEach(character => {
            characters[character.id] = character;
            conversations[character.id] = [];
            characterHistory[character.id] = [];
        });

        renderCharacters();

        if (data.length > 0) {
            const defaultCharacter = data[0];
            selectCharacter(defaultCharacter.id, defaultCharacter, false);
        }
    } catch (error) {
        console.error('Error loading characters:', error);
        const listEl = document.getElementById('characters-list');
        listEl.innerHTML = '<div style="color: var(--muted-color); font-size: 12px; text-align: center; padding: 20px;">酒馆尚未开门，后端可能未启动。</div>';
    }
}

/* ============ 渲染角色列表 ============ */
function renderCharacters() {
    const listEl = document.getElementById('characters-list');
    listEl.innerHTML = '';

    Object.values(characters).forEach(character => {
        const card = document.createElement('button');
        card.type = 'button';
        card.className = 'character-card';
        card.dataset.characterId = character.id;

        card.innerHTML = `
            <span class="character-avatar">${character.avatar || '🍺'}</span>
            <div class="character-meta">
                <div class="character-name">${character.name}</div>
                <div class="character-role">${character.role}</div>
            </div>
        `;

        card.addEventListener('click', () => selectCharacter(character.id, character, true));
        listEl.appendChild(card);
    });
}

/* ============ 选择角色 ============ */
function selectCharacter(characterId, character, shouldClearHistory = true) {
    currentCharacterId = characterId;
    currentExpression = 'normal';

    document.querySelectorAll('.character-card').forEach(card => {
        card.classList.toggle('active', card.dataset.characterId === characterId);
    });

    // 更新立绘
    const portraitEl = document.getElementById('portrait-emoji');
    portraitEl.textContent = character.avatar || '🍺';
    portraitEl.classList.add('expression-change');
    setTimeout(() => portraitEl.classList.remove('expression-change'), 300);

    document.getElementById('portrait-name').textContent = character.name || '酒客';
    document.getElementById('portrait-role').textContent = character.role || '角色';
    document.getElementById('portrait-desc').textContent = character.description || '一位故事中的人。';
    document.getElementById('portrait-expression').textContent = 'normal';

    // 更新角色状态
    updateCharacterStatus(character);

    // 更新聊天头
    const header = document.getElementById('chat-header');
    header.innerHTML = `
        <div class="header-mini">当前角色</div>
        <h2>${character.name}</h2>
        <div class="header-desc">${character.description}</div>
    `;

    // 清空或恢复聊天
    const messages = document.getElementById('chat-messages');
    if (shouldClearHistory) {
        messages.innerHTML = '';
        conversations[characterId] = [];
    } else if (conversations[characterId].length > 0) {
        renderConversationHistory(characterId);
    }

    // 启用输入
    const input = document.getElementById('message-input');
    const button = document.getElementById('send-button');
    input.disabled = false;
    button.disabled = false;
    input.focus();

    // 重置表情按钮
    updateExpressionButtons();
}

/* ============ 更新角色状态 ============ */
function updateCharacterStatus(character) {
    // 这里可以根据角色属性动态设置
    const moods = ['平静', '沉思', '愉快', '忧愁'];
    const postures = ['站立', '坐下', '倚靠', '凝视'];

    document.getElementById('char-mood').textContent = moods[Math.floor(Math.random() * moods.length)];
    document.getElementById('char-posture').textContent = postures[Math.floor(Math.random() * postures.length)];
    document.getElementById('char-focus').textContent = character.name ? `${character.name}` : '你';
}

/* ============ 表情切换 ============ */
function changeExpression(expression) {
    currentExpression = expression;
    const portraitEl = document.getElementById('portrait-emoji');
    portraitEl.classList.add('expression-change');
    setTimeout(() => portraitEl.classList.remove('expression-change'), 300);

    document.getElementById('portrait-expression').textContent = expression;
    updateExpressionButtons();
}

function updateExpressionButtons() {
    document.querySelectorAll('.expr-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.expr === currentExpression);
    });
}

/* ============ 发送消息 ============ */
async function sendMessage() {
    const input = document.getElementById('message-input');
    const button = document.getElementById('send-button');
    const message = input.value.trim();

    if (!message || !currentCharacterId) return;

    addMessageToUI('user', message);
    input.value = '';
    input.disabled = true;
    button.disabled = true;
    autoResizeTextarea();

    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                character_id: currentCharacterId,
                message: message
            })
        });

        const data = await response.json();

        if (data && data.success) {
            const responseText = data.message || '…';
            addMessageToUI('assistant', responseText);
            // 保存到历史
            saveToHistory(currentCharacterId, 'assistant', responseText);
        } else {
            addMessageToUI('assistant', data && data.error ? data.error : '酒馆里的灯忽然暗了一下。');
        }
    } catch (error) {
        console.error('Error sending message:', error);
        addMessageToUI('assistant', '酒馆的门外有风，后端似乎没在这里等你。');
    } finally {
        input.disabled = false;
        button.disabled = false;
        input.focus();
    }
}

/* ============ 添加消息到 UI ============ */
function addMessageToUI(role, content) {
    const messages = document.getElementById('chat-messages');
    const wrap = document.createElement('div');
    wrap.className = `message-row ${role}`;

    const bubble = document.createElement('div');
    bubble.className = `message-bubble ${role}`;
    bubble.textContent = content;

    wrap.appendChild(bubble);
    messages.appendChild(wrap);
    messages.scrollTop = messages.scrollHeight;

    // 保存到历史
    if (role === 'user') {
        saveToHistory(currentCharacterId, 'user', content);
    }
}

/* ============ 历史记录 ============ */
function saveToHistory(characterId, role, message) {
    if (!characterHistory[characterId]) {
        characterHistory[characterId] = [];
    }
    characterHistory[characterId].push({ role, message, timestamp: new Date() });
}

function renderConversationHistory(characterId) {
    const messages = document.getElementById('chat-messages');
    messages.innerHTML = '';
    const history = conversations[characterId] || [];

    history.forEach(item => {
        addMessageToUI(item.role, item.content);
    });
}

function renderHistoryPanel() {
    const content = document.getElementById('history-content');
    content.innerHTML = '';

    const history = characterHistory[currentCharacterId] || [];

    if (history.length === 0) {
        content.innerHTML = '<div style="color: var(--muted-color); text-align: center; padding: 20px; font-size: 12px;">暂无对话记录。</div>';
        return;
    }

    history.forEach(item => {
        const itemEl = document.createElement('div');
        itemEl.className = 'history-item';
        itemEl.innerHTML = `
            <div class="history-item-role">${item.role === 'user' ? '你' : characters[currentCharacterId].name}</div>
            <div class="history-item-text">${item.message}</div>
        `;
        content.appendChild(itemEl);
    });
}

/* ============ 场景切换 ============ */
function changeScene(scene) {
    currentScene = scene;
    // 这里可以继续扩展：改变背景、音乐等
    console.log('Scene changed to:', scene);
}

/* ============ 文本框自适应 ============ */
function autoResizeTextarea() {
    const input = document.getElementById('message-input');
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 180) + 'px';
}

/* ============ 事件监听 ============ */
function setupEventListeners() {
    // 发送消息
    document.getElementById('send-button').addEventListener('click', sendMessage);
    document.getElementById('message-input').addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
        autoResizeTextarea();
    });

    // 场景切换
    document.getElementById('scene-selector').addEventListener('change', (e) => {
        changeScene(e.target.value);
    });

    // 表情切换
    document.querySelectorAll('.expr-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            changeExpression(btn.dataset.expr);
        });
    });

    // 历史记录面板
    const historyPanel = document.getElementById('history-panel');
    document.getElementById('history-btn').addEventListener('click', () => {
        renderHistoryPanel();
        historyPanel.classList.toggle('hidden');
    });

    document.getElementById('close-history').addEventListener('click', () => {
        historyPanel.classList.add('hidden');
    });

    // 文本框自适应
    const textarea = document.getElementById('message-input');
    textarea.addEventListener('input', autoResizeTextarea);
}

/* ============ 启动 ============ */
window.addEventListener('DOMContentLoaded', init);
