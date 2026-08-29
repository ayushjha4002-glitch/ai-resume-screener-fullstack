# 🤖 AI Resume Screener

An AI-powered Resume Screening System that analyzes resumes against a Job Description (JD), extracts relevant information using LLMs, and generates a match score with a concise evaluation.

---

## 📌 Features

- 📄 Supports PDF and DOCX resumes
- 🧠 AI-powered Resume & Job Description parsing
- 🎯 Skill matching between resume and job description
- 📊 Match score generation
- 📝 Candidate summary with strengths and gaps
- ⚡ Built using Groq API for fast inference

---

## 🛠 Tech Stack

- Python
- Groq API
- Pydantic
- PyPDF2
- python-docx
- dotenv

---

## 📂 Project Structure

```
AI-Resume-Screener/
│
├── resumes/
│   ├── Resume1.pdf
│   └── Resume2.pdf
│
├── app.py
├── config.py
├── matcher.py
├── models.py
├── parser.py
├── prompts.py
├── reader.py
├── requirements.txt
├── README.md
└── .env
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/ayushjha4002-glitch/ai-resume-screener.git
```

Go into the project

```bash
cd ai-resume-screener
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file.

```
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Run

```bash
python app.py
```

---

## 📊 Example Output

```
Candidate: Jason Miller

Match Score: 10%

Summary:
Candidate has basic technical exposure but lacks most backend Python skills required for this role.
```

---

## 🚀 Future Improvements

- Streamlit Web Interface
- Batch Resume Processing
- Export Results to Excel
- Skill Gap Visualization
- Recruiter Dashboard
- Resume Ranking

---

## 👨‍💻 Author

**Ayush Jha**

B.Tech CSE Student

Passionate about AI, Software Development, and Data Structures & Algorithms.

GitHub:
https://github.com/ayushjha4002-glitch