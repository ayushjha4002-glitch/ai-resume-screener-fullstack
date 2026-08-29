# How to run this project (beginner-friendly)

Your project now has 3 pieces:

1. **The AI logic** (unchanged, your original code) — `reader.py`, `parser.py`, `matcher.py`, `models.py`, `prompts.py`, `config.py`
2. **The backend API** (new) — `api.py`. This is what makes your Python code reachable from a webpage.
3. **The frontend** (new) — `frontend/index.html`. One single file. No installs, no build step.

You need BOTH the backend and frontend running at the same time. Two terminal windows.

---

## Part 1 — Backend (terminal window #1)

1. Open a terminal in this project folder.
2. Create a virtual environment and install the dependencies:
   ```
   python -m venv .venv
   source .venv/bin/activate        # on Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Get a free Groq API key at https://console.groq.com/keys (sign up, click "Create API Key").
4. In the project folder, create a file named exactly `.env` with this one line inside:
   ```
   GROQ_API_KEY=paste_your_key_here
   ```
5. Start the server:
   ```
   uvicorn api:app --reload --port 8000
   ```
6. Leave this terminal open. Check it worked by opening http://localhost:8000/api/health in your
   browser — you should see `{"status":"ok"}`.

## Part 2 — Frontend (terminal window #2, or just your file explorer)

You have two options — try option A first, it's simpler:

**Option A:** Just double-click `frontend/index.html`. It'll open in your browser and should work.

**Option B (if A shows a blank page or errors):** Some browsers block local pages from calling
external websites. Serve it instead:
```
cd frontend
python -m http.server 5500
```
Then open http://localhost:5500 in your browser.

## Part 3 — Use it

1. Click one of the sample job description chips (or paste your own).
2. Drag a resume (PDF or DOCX) onto the drop zone, or click it to browse.
3. Click "Screen candidates".
4. Click any candidate row to see the full breakdown — matched skills, missing skills, AI summary.

If something goes wrong, check terminal window #1 (the backend) — errors will print there.

---

# Deploying it (so you have a live link for your resume/portfolio)

This is optional but makes a much stronger portfolio piece than "clone my repo and run it."

## Deploy the backend (Render, free tier)

1. Push this whole folder to a GitHub repo (if it isn't already).
2. Go to https://render.com, sign up, click "New +" → "Web Service", connect your GitHub repo.
3. Set:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn api:app --host 0.0.0.0 --port $PORT`
4. Under "Environment", add `GROQ_API_KEY` with your real key as the value.
5. Deploy. Render gives you a URL like `https://your-app.onrender.com` — test it by visiting
   `https://your-app.onrender.com/api/health`.

(Free tier note: the server "sleeps" after inactivity and takes ~30 seconds to wake up on the
first request — mention this if you demo it live, it's normal.)

## Deploy the frontend (Netlify, free, drag-and-drop)

1. Open `frontend/index.html` in a text editor and change this line near the top of the
   `<script type="text/babel">` block:
   ```js
   const API_URL = "http://localhost:8000";
   ```
   to your Render URL:
   ```js
   const API_URL = "https://your-app.onrender.com";
   ```
2. Go to https://app.netlify.com/drop
3. Drag the `frontend` folder onto the page. That's it — Netlify gives you a live URL instantly.

Now you have a real, live, working link you can put on your resume.

---

# Talking about this project in interviews

Quick framing you can use:

- **What it does:** Takes a job description and a batch of resumes, uses an LLM (via Groq) to
  extract structured data from both, then scores each candidate and explains the match — matched
  skills, missing skills, a written summary.
- **Architecture:** Python backend (FastAPI) wrapping an AI pipeline (read → parse → match),
  talking to a plain React frontend over a REST API (multipart file upload → JSON response).
- **Why no build tooling on the frontend:** deliberate choice to keep it simple and fully
  understandable end-to-end — React loaded via CDN, JSX compiled in-browser with Babel. You can
  say you know this trades off production performance for simplicity, and that a bundler (Vite)
  would be the next step for a production version.
- **Interesting problems you solved:** structured extraction from unstructured text (resumes) via
  LLM + Pydantic schemas, handling multiple file uploads with partial failure (one bad resume
  shouldn't break the whole batch — see the `errors` list in the API response), CORS between a
  separately-hosted frontend and backend.
