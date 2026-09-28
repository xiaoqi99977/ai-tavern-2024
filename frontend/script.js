const API_BASE_URL = 'http://localhost:5000/api';

let currentCharacterId = null;
const characters = {};
const conversations = {};

// Initialize the application
async function init() {
    await loadCharacters();
}

// Load characters from backend
async function loadCharacters() {
    try {
        const response = await fetch(`${API_BASE_URL}/characters`);
        const data = await response.json();
        
        data.forEach(character => {
            characters[character.id] = character;
            conversations[character.id] = [];
        });
        
        renderCharacters();
    } catch (error) {
        console.error('Error loading characters:', error);
        alert('Failed to load characters. Make sure the backend is running.');
    }
}

// Render characters list
function renderCharacters() {
    const charactersList = document.getElementById('characters-list');
    charactersList.innerHTML = '';
    
    Object.values(characters).forEach(character => {
        const card = document.createElement('div');
        card.className = 'character-card';
        card.innerHTML = `
            <div class="character-avatar">${character.avatar}</div>
            <div class="character-name">${character.name}</div>
            <div class="character-role">${character.role}</div>
            <div class="character-desc">${character.description}</div>
        `;
        
        card.addEventListener('click', () => selectCharacter(character.id, character));
        charactersList.appendChild(card);
    });
}

// Select a character
function selectCharacter(characterId, character) {
    currentCharacterId = characterId;
    
    // Update UI
    document.querySelectorAll('.character-card').forEach(card => {
        card.classList.remove('active');
    });
    event.target.closest('.character-card').classList.add('active');
    
    // Update chat header
    const chatHeader = document.getElementById('chat-header');
    chatHeader.innerHTML = `
        <div style="font-size: 2em; margin-bottom: 10px;">${character.avatar}</div>
        <h2>${character.name}</h2>
        <p>${character.description}</p>
    `;
    
    // Clear chat messages
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML = '';
    
    // Enable input
    document.getElementById('message-input').disabled = false;
    document.getElementById('send-button').disabled = false;
    document.getElementById('message-input').focus();
}

// Send message
async function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    
    if (!message || !currentCharacterId) return;
    
    // Add user message to UI
    addMessage('user', message);
    input.value = '';
    
    // Disable input while waiting for response
    input.disabled = true;
    document.getElementById('send-button').disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                character_id: currentCharacterId,
                message: message
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessage('assistant', data.message);
        } else {
            addMessage('assistant', `Error: ${data.error || 'Unknown error'}`);
        }
    } catch (error) {
        console.error('Error sending message:', error);
        addMessage('assistant', 'Connection error. Make sure the backend is running.');
    } finally {
        // Re-enable input
        input.disabled = false;
        document.getElementById('send-button').disabled = false;
        input.focus();
    }
}

// Add message to chat
function addMessage(role, content) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    messageDiv.innerHTML = `<div class="message-content">${escapeHtml(content)}</div>`;
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Event listeners
document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('message-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// Initialize on load
window.addEventListener('DOMContentLoaded', init);
