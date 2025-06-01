document.addEventListener("DOMContentLoaded", function () {
    const chatItems = document.querySelectorAll(".single-chat");

    chatItems.forEach(item => {
        item.addEventListener("click", async () => {
            const chatId = item.dataset.chatId;
            const chatName = item.dataset.chatName;

            document.getElementById("chat-title").textContent = chatName;
            document.getElementById("current-chat-id").textContent = chatId;
            document.getElementById("current-chat-name").textContent = chatName;

            try {
                const res = await fetch(`/chats/${chatId}/messages/`);
                const messages = await res.json();
                displayMessages(messages);
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
            <div class="suggestion-chat-name">${result.chat_name}</div>
        `;

        li.addEventListener('click', async () => {
            input.value = '';
            suggestionBox.innerHTML = '';

            document.getElementById("chat-title").textContent = result.is_group === false ? result.name : result.chat_name;
            document.getElementById("current-user-id").textContent = result.id;
            document.getElementById("current-chat-id").textContent = result.chat_id;
            document.getElementById("current-chat-name").textContent = result.chat_name;

            try {
                const res = await fetch(`/chats/${result.chat_id}/messages/`);
                const messages = await res.json();
                displayMessages(messages);
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
    const receiverId = document.getElementById("current-user-id").textContent;

    if (!text || !senderId) return;

    const response = await fetch(`/chats/messages/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: chatId, sender_id: senderId, text: text, receiver_id: receiverId})
    });

    if (response.ok) {
        const data = await response.json();
        chatId_new = data.chat_id;
    } else {
        console.error("Failed to send message");
    }

    document.getElementById("current-chat-id").textContent = chatId_new;
    input.value = '';
    try {
        const res = await fetch(`/chats/${chatId_new}/messages/`);
        const messages = await res.json();
        displayMessages(messages);
    } catch (err) {
        console.error("Failed to reload messages after sending:", err);
    }
});

function displayMessages(messages) {
    const container = document.getElementById("messages-container");
    container.innerHTML = '';

    messages.forEach(msg => {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message');

        if (msg.sender_id === CURRENT_USER_ID) {
            msgDiv.classList.add('message-right');
        } else {
            msgDiv.classList.add('message-left');
        }

        msgDiv.innerHTML = `
            <strong>${msg.user_name || msg.sender_id}</strong>: ${msg.text}
        `;

        container.appendChild(msgDiv);
    });

    container.scrollTop = container.scrollHeight;
}



