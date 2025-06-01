let socket;
let currentRoomId = null;

function joinChatRoom(chatId) {
    if (socket) {
        socket.close();
    }

    currentRoomId = chatId;

    socket = new WebSocket(`ws://${location.host}/ws/${chatId}`);

    socket.onmessage = function (event) {
        const message = JSON.parse(event.data);
        appendMessage(message);
    };

    socket.onclose = function () {
        console.log("WebSocket closed");
    };
}

function appendMessage(msg) {
    const container = document.getElementById("messages-container");

    if (msg.user_name == undefined || msg.user_name === undefined) return;

    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message');

    if (msg.sender_id === CURRENT_USER_ID) {
        msgDiv.classList.add('message-right');
    } else {
        msgDiv.classList.add('message-left');
    }

    msgDiv.innerHTML = `<strong>${msg.user_name || msg.sender_id}</strong>: ${msg.text}<br>hueta`;

    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;
}

window.joinChatRoom = joinChatRoom;
