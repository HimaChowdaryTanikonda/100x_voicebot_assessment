import os

try:
	import openai
except Exception:
	openai = None


def get_response(question: str) -> str:
	"""Return a text response for the provided question.

	Behavior:
	- If `OPENAI_API_KEY` (or `AI_API_KEY`) is present and `openai` package is available,
	  call the ChatCompletion API (gpt-3.5-turbo) and return the model reply.
	- Otherwise, use a small deterministic fallback tailored to common interview questions
	  so the app works without any API keys (user-friendly demo).
	"""
	key = os.getenv("OPENAI_API_KEY") or os.getenv("AI_API_KEY")
	q = (question or "").strip()

	if key and openai:
		openai.api_key = key
		messages = [
			{
				"role": "system",
				"content": (
					"You are a concise, friendly assistant answering interview-style personal "
					"questions in the first person as if you were the candidate. Keep answers clear "
					"and approachable for non-technical users."
				),
			},
			{"role": "user", "content": q},
		]

		resp = openai.ChatCompletion.create(
			model="gpt-3.5-turbo", messages=messages, max_tokens=300, temperature=0.7
		)
		return resp["choices"][0]["message"]["content"].strip()

	# Fallback deterministic responses (no API key required)
	ql = q.lower()
	if "life story" in ql or "what should we know" in ql or "few sentences" in ql:
		return (
			"I grew up curious about technology, studied engineering, and now build helpful AI "
			"demos. I enjoy learning, mentoring others, and turning complex topics into simple, "
			"actionable steps."
		)

	if "superpower" in ql:
		return (
			"My #1 superpower is making complex ideas clear and actionable — I simplify problems "
			"and create practical next steps people can follow."
		)

	if "top 3" in ql or "top three" in ql or "areas you'd like to grow" in ql:
		return (
			"1) Communicating technical ideas to non-technical audiences. "
			"2) Building scalable, production-grade systems. "
			"3) Improving testing and long-term maintainability."
		)

	if "misconception" in ql or "coworkers" in ql:
		return (
			"A common misconception is that I'm quiet or reserved — in reality I collaborate closely, "
			"ask lots of questions, and prefer iterative feedback cycles."
		)

	if "push your boundaries" in ql or "push your limits" in ql:
		return (
			"I push my boundaries by taking on projects outside my comfort zone, pairing with experts, "
			"and breaking big goals into small experiments that build confidence over time."
		)

	# Generic fallback answer with instructions on enabling the OpenAI path
	return (
		"I’m a concise, helpful assistant. Try asking interview-style questions like: "
		"'What’s your #1 superpower?' or 'What should we know about your life story in a few sentences?'. "
		"For richer answers, set the OPENAI_API_KEY environment variable and restart the backend."
	)

