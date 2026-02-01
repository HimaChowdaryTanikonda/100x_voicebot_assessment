const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");
const questionEl = document.getElementById("question");
const responseEl = document.getElementById("response");

let recognition;

function supportsSpeechRecognition() {
	return !!(window.SpeechRecognition || window.webkitSpeechRecognition);
}

if (supportsSpeechRecognition()) {
	const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
	recognition = new SR();
	recognition.lang = 'en-US';
	recognition.interimResults = false;

	recognition.onresult = (ev) => {
		const text = Array.from(ev.results).map(r => r[0].transcript).join('');
		questionEl.textContent = text;
		sendQuestion(text);
	};

	recognition.onend = () => {
		recordBtn.disabled = false;
		stopBtn.disabled = true;
	};
} else {
	recordBtn.disabled = true;
	questionEl.textContent = 'Speech recognition not supported in this browser.';
}

recordBtn.addEventListener('click', () => {
	if (!recognition) return;
	recordBtn.disabled = true;
	stopBtn.disabled = false;
	questionEl.textContent = '(listening...)';
	recognition.start();
});

stopBtn.addEventListener('click', () => {
	if (!recognition) return;
	recognition.stop();
});

async function sendQuestion(text) {
	responseEl.textContent = 'Thinking...';
	try {
		const res = await fetch('http://localhost:5000/api/ask', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ question: text }),
		});
		const data = await res.json();
		if (data.error) {
			responseEl.textContent = 'Error: ' + data.error;
			return;
		}
		const answer = data.answer;
		responseEl.textContent = answer;
		speak(answer);
	} catch (err) {
		responseEl.textContent = 'Network error: ' + err.message;
	}
}

function speak(text) {
	if (!('speechSynthesis' in window)) return;
	const utter = new SpeechSynthesisUtterance(text);
	utter.lang = 'en-US';
	window.speechSynthesis.cancel();
	window.speechSynthesis.speak(utter);
}
