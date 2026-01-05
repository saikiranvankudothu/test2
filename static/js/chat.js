// static/js/chat.js

let chatInitialized = false;

window.sendChat = async function () {
  const input = document.getElementById("chatInput");
  const question = input.value.trim();
  if (!question) return;

  if (!chatInitialized) {
    document.getElementById("chatBox").innerHTML = "";
    chatInitialized = true;
  }

  appendUserMessage(question);
  input.value = "";

  const form = new URLSearchParams();
  form.append("question", question);

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: form,
    });

    const data = await res.json();
    appendBotMessage(data.answer);
  } catch {
    appendBotMessage("Error contacting server.");
  }
};

function appendUserMessage(msg) {
  const box = document.getElementById("chatBox");
  box.innerHTML += `<div class="message user-msg">${escapeHtml(msg)}</div>`;
  box.scrollTop = box.scrollHeight;
}

function appendBotMessage(msg) {
  const box = document.getElementById("chatBox");
  box.innerHTML += `<div class="message bot-msg">${escapeHtml(msg)}</div>`;
  box.scrollTop = box.scrollHeight;
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("chatInput").addEventListener("keypress", (e) => {
    if (e.key === "Enter") window.sendChat();
  });
});
