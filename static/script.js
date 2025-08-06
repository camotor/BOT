document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const sidebar = document.getElementById('sidebar');
    const sessionsList = document.getElementById('sessions-list');
    const newChatBtn = document.getElementById('new-chat-btn');
    const menuBtn = document.getElementById('menu-btn');
    const toggleSidebarBtn = document.getElementById('toggle-sidebar');
    const renameSessionBtn = document.getElementById('rename-session-btn');
    const deleteSessionBtn = document.getElementById('delete-session-btn');
    const renameModal = document.getElementById('rename-modal');
    const sessionTitleInput = document.getElementById('session-title-input');
    const saveTitleBtn = document.getElementById('save-title-btn');
    const cancelRenameBtn = document.getElementById('cancel-rename-btn');

    let currentSessionId = null;
    let sessions = [];

    const addMessage = (message, sender, timestamp = null) => {
        // Remover mensaje de bienvenida si existe
        const welcomeMessage = chatBox.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }

        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', `${sender}-message`);
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.innerHTML = message;
        
        messageElement.appendChild(messageContent);
        
        if (timestamp) {
            const timeElement = document.createElement('div');
            timeElement.classList.add('message-time');
            timeElement.textContent = new Date(timestamp).toLocaleTimeString();
            messageElement.appendChild(timeElement);
        }
        
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    const clearChat = () => {
        chatBox.innerHTML = '<div class="welcome-message"><h3>¡Bienvenido al Chat con Gemini!</h3><p>Inicia una conversación o selecciona un chat anterior del historial.</p></div>';
    };

    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (message === '') return;

        addMessage(message, 'user');
        userInput.value = '';

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message,
                    session_id: currentSessionId 
                }),
            });

            const data = await response.json();
            
            if (data.error) {
                addMessage('Error: ' + data.error, 'bot');
                return;
            }

            addMessage(data.reply, 'bot');
            
            // Actualizar session_id si es nueva
            if (!currentSessionId) {
                currentSessionId = data.session_id;
                loadSessions(); // Recargar lista de sesiones
            }
            
        } catch (error) {
            console.error('Error:', error);
            addMessage('Lo siento, algo salió mal.', 'bot');
        }
    };

    const loadSessions = async () => {
        try {
            const response = await fetch('/api/sessions');
            const data = await response.json();
            sessions = data.sessions;
            renderSessions();
        } catch (error) {
            console.error('Error loading sessions:', error);
        }
    };

    const renderSessions = () => {
        sessionsList.innerHTML = '';
        
        sessions.forEach(session => {
            const sessionElement = document.createElement('div');
            sessionElement.classList.add('session-item');
            if (session.session_id === currentSessionId) {
                sessionElement.classList.add('active');
            }
            
            sessionElement.innerHTML = `
                <div class="session-title">${session.title}</div>
                <div class="session-info">
                    <span class="message-count">${session.message_count} mensajes</span>
                    <span class="session-date">${new Date(session.last_activity).toLocaleDateString()}</span>
                </div>
            `;
            
            sessionElement.addEventListener('click', () => loadSession(session.session_id));
            sessionsList.appendChild(sessionElement);
        });
    };

    const loadSession = async (sessionId) => {
        try {
            const response = await fetch(`/api/sessions/${sessionId}/messages`);
            const data = await response.json();
            
            currentSessionId = sessionId;
            clearChat();
            
            data.messages.forEach(msg => {
                addMessage(msg.content, msg.type, msg.timestamp);
            });
            
            renderSessions(); // Actualizar UI para mostrar sesión activa
            
            // Ocultar sidebar en móvil después de seleccionar
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('open');
            }
            
        } catch (error) {
            console.error('Error loading session:', error);
        }
    };

    const createNewSession = async () => {
        try {
            const response = await fetch('/api/sessions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title: null }),
            });
            
            const data = await response.json();
            currentSessionId = data.session_id;
            clearChat();
            loadSessions();
            
            // Ocultar sidebar en móvil
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('open');
            }
            
        } catch (error) {
            console.error('Error creating session:', error);
        }
    };

    const deleteCurrentSession = async () => {
        if (!currentSessionId) return;
        
        if (confirm('¿Estás seguro de que quieres eliminar esta sesión?')) {
            try {
                await fetch(`/api/sessions/${currentSessionId}`, {
                    method: 'DELETE',
                });
                
                currentSessionId = null;
                clearChat();
                loadSessions();
                
            } catch (error) {
                console.error('Error deleting session:', error);
            }
        }
    };

    const renameCurrentSession = async () => {
        if (!currentSessionId) return;
        
        const currentSession = sessions.find(s => s.session_id === currentSessionId);
        if (currentSession) {
            sessionTitleInput.value = currentSession.title;
            renameModal.style.display = 'flex';
        }
    };

    const saveSessionTitle = async () => {
        const newTitle = sessionTitleInput.value.trim();
        if (!newTitle || !currentSessionId) return;
        
        try {
            await fetch(`/api/sessions/${currentSessionId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title: newTitle }),
            });
            
            renameModal.style.display = 'none';
            loadSessions();
            
        } catch (error) {
            console.error('Error updating session title:', error);
        }
    };

    // Event listeners
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    newChatBtn.addEventListener('click', createNewSession);
    deleteSessionBtn.addEventListener('click', deleteCurrentSession);
    renameSessionBtn.addEventListener('click', renameCurrentSession);
    
    menuBtn.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });
    
    toggleSidebarBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
    });

    saveTitleBtn.addEventListener('click', saveSessionTitle);
    cancelRenameBtn.addEventListener('click', () => {
        renameModal.style.display = 'none';
    });

    // Cerrar modal al hacer clic fuera
    renameModal.addEventListener('click', (e) => {
        if (e.target === renameModal) {
            renameModal.style.display = 'none';
        }
    });

    // Manejar redimensionamiento de ventana
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('open');
        }
    });

    // Cargar sesiones al iniciar
    loadSessions();
});
