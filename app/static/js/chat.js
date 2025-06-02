document.addEventListener("DOMContentLoaded", function () {
    const chatItems = document.querySelectorAll(".single-chat");

    const chatId = document.getElementById("current-chat-id").textContent;
    if (chatId) {
        fetch(`/chats/${chatId}/messages/`)
            .then(res => res.json())
            .then(messages => {
                displayMessages(messages);
                window.joinChatRoom(chatId);
            })
            .catch(err => console.error("Failed to load initial messages:", err));
    }

    chatItems.forEach(item => {
        item.addEventListener("click", async () => {
            initialLoad = true;
            console.log(item.dataset);
            const chatId = item.dataset.chatId;
            const chatName = item.dataset.chatName;
            const nickname = item.dataset.currentUserNickname;

            document.getElementById("chat-title").textContent = chatName;
            document.getElementById("current-user-nickname").textContent = "@" + nickname;
            document.getElementById("current-chat-id").textContent = chatId;
            document.getElementById("current-chat-name").textContent = chatName;
            document.getElementById("current-user-id").textContent = item.dataset.currentUserId;

            try {
                const res = await fetch(`/chats/${chatId}/messages/`);
                const messages = await res.json();
                displayMessages(messages);
                window.joinChatRoom(chatId);
            } catch (err) {
                console.error('Failed to load messages:', err);
            }
        });
    });

});

const input = document.getElementById('user-search-input');
const suggestionBox = document.getElementById('user-suggestions');

let debounceTimeout;

input.addEventListener('input', () => {
    const query = input.value.trim();
    clearTimeout(debounceTimeout);

    if (query.length === 0) {
        suggestionBox.innerHTML = '';
        return;
    }

    debounceTimeout = setTimeout(async () => {
        try {
            const res = await fetch(`/api/search_users?current_user_id=${CURRENT_USER_ID}&nickname=${encodeURIComponent(query)}`);
            const users = await res.json();
            renderSuggestions(users);
        } catch (err) {
            console.error('Error fetching users:', err);
        }
    }, 200);
});

function renderSuggestions(results) {
    suggestionBox.innerHTML = '';

    results.slice(0, 5).forEach(result => {
        const li = document.createElement('li');
        li.innerHTML = `
            <div class="suggestion-user-id" style="display: none;">${result.id}</div>
            <div class="suggestion-name">${result.name}</div>
            <div class="suggestion-nickname">@${result.nickname}</div>
        `;

        li.addEventListener('click', async () => {
            initialLoad = true;
            input.value = '';
            suggestionBox.innerHTML = '';

            document.getElementById("chat-title").textContent = result.is_group === false ? result.name : result.chat_name;
            document.getElementById("current-user-id").textContent = result.id;
            document.getElementById("current-chat-id").textContent = result.chat_id;
            document.getElementById("current-chat-name").textContent = result.chat_name;
            document.getElementById("current-user-nickname").textContent = "@" + result.nickname;

            try {
                const res = await fetch(`/chats/${result.chat_id}/messages/`);
                const messages = await res.json();
                displayMessages(messages);
                window.joinChatRoom(result.chat_id);
            } catch (err) {
                console.error('Failed to load messages:', err);
            }
        });

        suggestionBox.appendChild(li);
    });
}

document.getElementById("send-button").addEventListener("click", async () => {
    const input = document.getElementById("message-input");
    const text = input.value.trim();
    const chatId = document.getElementById("current-chat-id").textContent;
    const senderId = CURRENT_USER_ID;
    const receiverId = parseInt(document.getElementById("current-user-id").textContent, 10);
    console.log({ chat_id: chatId, sender_id: senderId, text: text, receiver_id: receiverId });
    if (!text || !senderId) return;
    const response = await fetch(`/chats/messages/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: chatId, sender_id: senderId, text: text, receiver_id: receiverId })
    });

    let chatId_new = chatId;

    if (response.ok) {
        const data = await response.json();
        chatId_new = data.chat_id;
    } else {
        console.error("Failed to send message");
    }

    document.getElementById("current-chat-id").textContent = chatId_new;
    document.getElementById("current-user-id").textContent = receiverId;
    input.value = '';

    try {
        const res = await fetch(`/chats/${chatId_new}/messages/`);
        const messages = await res.json();
        displayMessages(messages);
    } catch (err) {
        console.error("Failed to reload messages after sending:", err);
    }
});

let initialLoad = true;

function displayMessages(messages) {
    const container = document.getElementById("messages-container");

    const previousScroll = container.scrollTop;
    const previousHeight = container.scrollHeight;
    const isAtBottom = Math.abs(previousScroll + container.clientHeight - previousHeight) < 10;

    container.innerHTML = '';
    let lastDate = null;

    messages.forEach(msg => {
        if (!msg.user_name || !msg.text || !msg.timestamp) return;

        const [datePart, timePart] = msg.timestamp.split(' ');
        if (datePart !== lastDate) {
            const dateDiv = document.createElement('div');
            dateDiv.classList.add('date-divider');
            dateDiv.textContent = datePart;
            container.appendChild(dateDiv);
            lastDate = datePart;
        }

        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message');

        if (msg.sender_id === CURRENT_USER_ID) {
            msgDiv.classList.add('message-right');
            var msgSender = 'You';
        } else {
            msgDiv.classList.add('message-left');
            var msgSender = msg.user_name;
        }

        msgDiv.innerHTML = `<strong>${msgSender}</strong><br><br>${msg.text}<br><small style="font-size: 11px;">${timePart}</small>`;
        container.appendChild(msgDiv);
    });

    if (initialLoad || isAtBottom) {
        container.scrollTop = container.scrollHeight;
    }

    initialLoad = false;
}

setInterval(async () => {
    const chatId = document.getElementById("current-chat-id").textContent;
    if (!chatId) return;

    try {
        const res = await fetch(`/chats/${chatId}/messages/`);
        const messages = await res.json();
        displayMessages(messages);
    } catch (err) {
        console.error("Auto-refresh failed:", err);
    }
}, 3000);

document.getElementById("message-input").addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        document.getElementById("send-button").click();
    }
});
