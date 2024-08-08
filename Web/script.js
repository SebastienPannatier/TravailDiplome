async function sendMessage(message = null) {
  const inputField = document.getElementById("user-input");
  const userMessage = message || inputField.value;
  if (userMessage.trim() === "") return;

  displayMessage(userMessage, "user");

  const response = await fetch("http://localhost:5005/webhooks/rest/webhook", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ sender: "user", message: userMessage }),
  });

  const data = await response.json();
  data.forEach((msg) => {
    if (msg.text) {
      displayMessage(msg.text, "bot");
    }
    if (msg.buttons) {
      displayButtons(msg.buttons);
    }
  });

  inputField.value = "";
}

function displayMessage(message, sender) {
  const messagesContainer = document.getElementById("messages");
  const messageContainer = document.createElement("div");
  messageContainer.classList.add("message-container", sender);

  const icon = document.createElement("img");
  icon.classList.add("icon");
  icon.src = sender === "user" ? "sources/user.png" : "sources/robot.png";

  const messageElement = document.createElement("div");
  messageElement.classList.add("message", sender);
  messageElement.innerText = message;

  if (sender === "user") {
    messageContainer.appendChild(messageElement);
    messageContainer.appendChild(icon);
  } else {
    messageContainer.appendChild(icon);
    messageContainer.appendChild(messageElement);
  }

  messagesContainer.appendChild(messageContainer);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function displayButtons(buttons) {
  const messagesContainer = document.getElementById("messages");
  const buttonsContainer = document.createElement("div");
  buttonsContainer.classList.add("buttons-container");

  buttons.forEach((button) => {
    const buttonElement = document.createElement("button");
    buttonElement.innerText = button.title;
    buttonElement.onclick = () => sendMessage(button.payload);
    buttonsContainer.appendChild(buttonElement);
  });

  messagesContainer.appendChild(buttonsContainer);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
