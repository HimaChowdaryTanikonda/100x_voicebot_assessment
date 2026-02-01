# Copilot instructions — 100x Generative AI voice bot

Purpose
- Help AI coding agents quickly become productive in this repository by describing the project layout, run/debug steps, and where to make changes.

Big picture (what to know first)
- The repo is a minimal static frontend + backend layout:
  - Frontend static files: [frontend/index.html](frontend/index.html), [frontend/script.js](frontend/script.js), [frontend/style.css](frontend/style.css).
  - Backend implementation: [backend/app.py](backend/app.py) and domain logic in [backend/voicebot_logic.py](backend/voicebot_logic.py).
  - Project README: [README.md](README.md) contains the primary local run instructions.

What the codebase expects (discoverable facts)
- The README recommends running the backend with `pip install -r requirements.txt` and `python app.py` from the backend folder; follow that convention unless you find a different runner or package manifest.
- There are no tests, no package.json, and no obvious env var usage in repository files — check `backend/` for added requirements or config when implementing integrations.

Where to make changes (practical guidance)
- Add HTTP API endpoints and request handling in `backend/app.py` (this is the entrypoint area).
- Put AI integration, prompt construction, and response-formatting code in `backend/voicebot_logic.py` so business logic stays separate from transport code.
- Update the UI in `frontend/*` and call the backend endpoints from `frontend/script.js`.

Typical integration points
- AI / model calls should be implemented in the backend logic file and hidden behind a single API endpoint (e.g., `POST /api/ask`). Example flow:
  1. Frontend sends JSON {"question": "..."} -> `POST /api/ask`
  2. `backend/app.py` validates the request and calls `voicebot_logic.get_response(question)`
  3. `voicebot_logic.py` calls the AI provider, returns structured JSON to the frontend

Local dev workflow (explicit)
- From the repo root, run the backend by changing to the backend folder then install and run:
  ```bash
  cd backend
  pip install -r requirements.txt
  python app.py
  ```
- Open `frontend/index.html` in a browser (or serve `frontend/` via a static server) to test the UI against the running backend.

Project-specific conventions and checks
- The project separates transport (app.py) and business logic (voicebot_logic.py). Keep that separation.
- No test framework detected — add tests under `tests/` if you add core logic.
- Prefer environment variables for secrets. No `.env` or env-var usage found; when adding API keys use `OPENAI_API_KEY` or `AI_API_KEY` and document in README.

What to look for when editing
- If you add dependencies, update `backend/requirements.txt` and include exact versions.
- If you change API shapes, update `frontend/script.js` to match the new JSON contract.

If this file already exists
- Preserve prior content and merge: keep any project-specific rules or examples, then apply the concise guidance above.

Questions for the maintainer
- Confirm preferred backend framework (Flask, FastAPI, Express). If unspecified, prefer Flask for quick Python prototypes.
- Confirm preferred env var name for API keys and whether to add a `.env.example`.

If anything is unclear or you want a different structure, tell me which parts to expand or edit.
