// AI Chat Assistant JavaScript
// Consistent with Galaxy Neon Blue Theme

const chatIcon = document.getElementById('ai-chat-icon');
const chatWidget = document.getElementById('ai-chat-widget');
const closeBtn = document.getElementById('close-chat');
const sendBtn = document.getElementById('send-btn');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');

// Toggle chat widget on icon click
chatIcon.addEventListener('click', function() {
    chatWidget.style.display = chatWidget.style.display === 'flex' ? 'none' : 'flex';
});

// Close chat widget on close button click
closeBtn.addEventListener('click', function() {
    chatWidget.style.display = 'none';
    chatMessages.innerHTML = '<div class="ai-message">Hello! How can I help you with your expenses?</div>';
});

// Send message on button click
sendBtn.addEventListener('click', function() {
    sendMessage();
});

// Send message on Enter key
chatInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const message = chatInput.value.trim();
    if (message) {
        const userMessage = document.createElement('div');
        userMessage.className = 'user-message';
        userMessage.textContent = message;
        chatMessages.appendChild(userMessage);
        chatInput.value = '';

        // Send AJAX request to backend
        fetch('/ai-chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Include CSRF token if needed
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            const aiMessage = document.createElement('div');
            aiMessage.className = 'ai-message';
            aiMessage.textContent = data.response;
            chatMessages.appendChild(aiMessage);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        })
        .catch(error => {
            console.error('Error:', error);
            const aiMessage = document.createElement('div');
            aiMessage.className = 'ai-message';
            aiMessage.textContent = 'Sorry, I couldn\'t process your request.';
            chatMessages.appendChild(aiMessage);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
    }
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
