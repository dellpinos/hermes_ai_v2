
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('#chat-messages')) {
        const chatMessages = document.getElementById('chat-messages');
        const chatInputBox = document.getElementById('chat-input-box');
        const sendButton = document.getElementById('send-button');

        const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        const chatToken = crypto.randomUUID().replace(/-/g, "").slice(0, 32);

        console.log(chatToken)


        sendButton.addEventListener('click', sendMessage);
        chatInputBox.addEventListener('keypress', function (e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        async function sendMessage() {
            const messageText = chatInputBox.value.trim();
            if (messageText === '' || messageText.length > 600) return;

            // Agregar el mensaje del usuario a la interfaz
            addMessageToUI(messageText, 'user');

            // Limpiar y bloquear el cuadro de entrada
            chatInputBox.disabled = true;
            chatInputBox.value = '';

            showLoader();

            // Enviar mensaje
            const formData = new FormData();
            formData.append("message", messageText);
            formData.append("token", chatToken);

            try {
                const url = '/api/chat/';
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': csrftoken,
                    }
                });

                const result = await response.json();
                addMessageToUI(result.response, 'ai');

            } catch (error) {
                console.log(error);
            } finally {

                hideLoader();
                chatInputBox.disabled = false;
                chatInputBox.focus = true;
            }

        }


        function addMessageToUI(text, sender) {
            const messageElement = document.createElement('div');
            messageElement.classList.add('chat__msg-wrapper');
            // messageElement.textContent = text;

            const textMsg = document.createElement('P');
            textMsg.classList.add('chat__msg');
            textMsg.textContent = text;

            if (sender === 'user') {
                messageElement.classList.add('chat__msg-wrapper--user');
                textMsg.classList.add('chat__msg--user');
            } else {
                messageElement.classList.add('chat__msg-wrapper--ai');
                textMsg.classList.add('chat__msg--ai');
            }

            messageElement.appendChild(textMsg);
            chatMessages.appendChild(messageElement);

            // Desplazar hacia abajo para ver el último mensaje
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function showLoader() {

            const messageElement = document.createElement('div');
            messageElement.classList.add('loader-wrapper');

            const loader = document.createElement('div');
            loader.style = 'display:flex; gap:20px; align-items:center;'
            loader.id = 'loader';
            loader.innerHTML = '<span class="loader"></span><p>Destilando conocimiento . . .</p>';

            messageElement.appendChild(loader);
            document.getElementById('chat-messages').appendChild(messageElement);

            // Desplazar hacia abajo para ver el último mensaje
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function hideLoader() {
            const loader = document.querySelector('.loader-wrapper');
            if (!loader) return;

            while (loader.firstChild) {
                loader.firstChild.remove();
            }
            loader.remove();
        }
    }
})
