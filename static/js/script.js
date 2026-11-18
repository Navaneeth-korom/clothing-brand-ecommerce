const form = document.getElementById("chat-form");
const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
const input = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const conversation = document.getElementById("conversation");
const requestStatus = document.getElementById("request-status");

function scrollToLatest() {
    conversation.scrollTop = conversation.scrollHeight;
}

function appendMessage(text, sender) {
    const row = document.createElement("div");
    row.className = `message-row ${sender}`;

    if (sender === "assistant") {
        const avatar = document.createElement("span");
        avatar.className = "assistant-avatar";
        avatar.setAttribute("aria-hidden", "true");
        avatar.textContent = "✦";
        row.append(avatar);
    }

    const bubble = document.createElement("div");
    bubble.className = "message";
    bubble.textContent = text;
    row.append(bubble);
    conversation.append(row);
    scrollToLatest();
    return row;
}

async function sendMessage(text) {
    appendMessage(text, "user");
    input.disabled = true;
    sendButton.disabled = true;
    requestStatus.textContent = "Waiting for a reply.";

    const typingRow = document.createElement("div");
    typingRow.className = "message-row";
    typingRow.setAttribute("aria-label", "Assistant is typing");
    const typingBubble = document.createElement("div");
    typingBubble.className = "message";
    typingBubble.innerHTML = '<span class="typing" aria-hidden="true"><span></span><span></span><span></span></span>';
    typingRow.append(typingBubble);
    conversation.append(typingRow);
    scrollToLatest();

    try {
        const response = await fetch(form.action, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ message: text })
        });
        const data = await response.json();

        if (!response.ok) {
            const detail = Object.values(data).flat().join(" ");
            throw new Error(detail || "The message could not be sent. Please try again.");
        }

        if (typeof data.reply !== "string" || !data.reply.trim()) {
            throw new Error("The assistant returned an empty reply. Please try again.");
        }

        typingRow.remove();
        appendMessage(data.reply, "assistant");
        requestStatus.textContent = "Reply received.";
    } catch (error) {
        typingRow.remove();
        appendMessage(error.message || "Something went wrong. Please try again.", "assistant");
        requestStatus.textContent = "There was a problem sending your message.";
    } finally {
        input.disabled = false;
        sendButton.disabled = false;
        input.focus();
    }
}

form.addEventListener("submit", (event) => {
    event.preventDefault();
    const text = input.value.trim();
    if (!text || sendButton.disabled) return;
    input.value = "";
    sendMessage(text);
});
