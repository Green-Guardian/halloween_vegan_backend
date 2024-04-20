document.addEventListener('DOMContentLoaded', function () {
    document.body.classList.add('--dark-theme');

    var chatSocket = new WebSocket(
        (window.location.protocol === "https:" ? "wss://" : "ws://") + window.location.host + '/ws/app/chat/'
    );

    chatSocket.onmessage = function (e) {
        var data = JSON.parse(e.data);
        if (data.type === "chat_message" || data.type === "chat_history") {
            addMessage(data.message, data.user, data.status); // 'sent' или 'received'
        }
    };

    var sendMessage = function () {
        var messageInputDom = document.querySelector('.chat__conversation-panel__input');
        var message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    };

    document.querySelector('.send-message-button').addEventListener('click', function (e) {
        sendMessage();
    });

    document.querySelector('.chat__conversation-panel__input').addEventListener('keypress', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Функция для добавления сообщения в .chat__conversation-board
    function addMessage(message, user, status) {
        var chatLog = document.querySelector('.chat__conversation-board');

        var messageContainer = document.createElement('div');
        messageContainer.classList.add('chat__conversation-board__message-container');
        if (status === 'sent') {
            messageContainer.classList.add('reversed');
        }

        var avatarContainer = document.createElement('div');
        avatarContainer.classList.add('chat__conversation-board__message__person');

        var avatarImg = document.createElement('img');
        // Используйте статический URL для изображения аватара пользователя или дефолтный аватар
        avatarImg.src = "https://seal-pavel.website/halloween-vegan-backend-stage/static/app/favicon.ico";
        avatarImg.classList.add('chat__conversation-board__message__person__avatar');
        avatarContainer.appendChild(avatarImg);

        var messageTextContainer = document.createElement('div');
        messageTextContainer.classList.add('chat__conversation-board__message__context');

        var messageBubble = document.createElement('div');
        messageBubble.classList.add('chat__conversation-board__message__bubble');
        messageBubble.innerHTML = `<span>${message}</span>`;
        messageTextContainer.appendChild(messageBubble);

        messageContainer.appendChild(avatarContainer);
        messageContainer.appendChild(messageTextContainer);

        chatLog.appendChild(messageContainer);
        chatLog.scrollTop = chatLog.scrollHeight;
    }
});
