function startListening() {
  const status = document.getElementById("status");
  const answer = document.getElementById("answer");

  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    status.innerText = "❌ Speech recognition is not supported in this browser.";
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
      const res = await fetch(
        "100xvoicebotassessment-production-40cc.up.railway.app/ask",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question })
        }
      );

      // ✅ NEW: Check response status
      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();

      if (!data.answer) {
        throw new Error("No answer received from server");
      }

      answer.innerText = data.answer;

      const speech = new SpeechSynthesisUtterance(data.answer);
      speech.rate = 1;
      speech.pitch = 1;
      speech.lang = "en-US";
      speechSynthesis.speak(speech);

      status.innerText = `🗣️ You asked: "${question}"`;

    } catch (err) {
      console.error(err);
      status.innerText =
        "⚠️ Server is waking up or unavailable. Please try again in a few seconds.";
    }
  };

  recognition.onerror = () => {
    status.innerText = "❌ I couldn’t hear clearly. Please try again.";
  };
}

