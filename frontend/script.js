function startListening() {
  const status = document.getElementById("status");
  const answer = document.getElementById("answer");

  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    status.innerText = "Speech recognition is not supported in this browser.";
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.start();

  status.innerText = "🎧 Listening... Please speak now";
  answer.innerText = "";

  recognition.onresult = async (event) => {
    const question = event.results[0][0].transcript;
    status.innerText = "🤔 Thinking...";

    try {
      const res = await fetch("http://localhost:5000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
      });

      const data = await res.json();
      answer.innerText = data.answer;

      const speech = new SpeechSynthesisUtterance(data.answer);
      speech.rate = 1;
      speech.pitch = 1;
      speechSynthesis.speak(speech);

      status.innerText = `🗣️ You asked: "${question}"`;
    } catch (err) {
      status.innerText = "⚠️ Could not connect to the server.";
    }
  };

  recognition.onerror = () => {
    status.innerText = "❌ I couldn’t hear clearly. Please try again.";
  };
}
