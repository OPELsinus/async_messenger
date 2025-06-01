// chat_ws.js
let socket;
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;

export function connectWebSocket(userId, onMessageCallback) {
    socket = new WebSocket(`ws://${location.host}/ws/${userId}`);

    socket.onopen = () => {
        console.log("WebSocket connected");
        reconnectAttempts = 0;
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "new_message") {
            onMessageCallback(data.message);
        }
    };

    socket.onclose = () => {
        if (reconnectAttempts < maxReconnectAttempts) {
            setTimeout(() => {
                reconnectAttempts++;
                connectWebSocket(userId, onMessageCallback);
            }, 1000);
        }
    };
}

export function sendChatMessage(chatId, text, senderId) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: "send_message",
            chat_id: chatId,
            text: text,
            sender_id: senderId
        }));
    }
}

export function joinChatRoom(chatId) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: "join_chat",
            chat_id: chatId
        }));
    }
}