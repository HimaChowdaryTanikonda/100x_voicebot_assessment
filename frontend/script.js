const recordBtn = document.getElementById("recordBtn");
const userText = document.getElementById("userText");
const botText = document.getElementById("botText");

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";

recordBtn.onclick = () => {
  recognition.start();
};

recognition.onresult = async (event) => {
  const transcript = event.results[0][0].transcript;
  userText.innerText = transcript;

  const response = await fetch("http://127.0.0.1:5000/api/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ question: transcript })
  });

  const data = await response.json();
  botText.innerText = data.answer;

  const utterance = new SpeechSynthesisUtterance(data.answer);
  speechSynthesis.speak(utterance);
};
