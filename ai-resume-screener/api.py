"""
FastAPI wrapper around the existing screening pipeline.

This file does not change any of the original logic in reader.py,
parser.py, matcher.py, or models.py — it just exposes them over HTTP
so a frontend (or any other client) can call them.

Run with:
    uvicorn api:app --reload --port 8000
"""

import shutil
import tempfile
import uuid
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from matcher import match_resume
from parser import parse_job_description, parse_resume
from reader import read_resume

ALLOWED_SUFFIXES = {".pdf", ".docx"}
JD_FOLDER = Path(__file__).resolve().parent / "job_descriptions"

app = FastAPI(title="AI Resume Screener API")

# Wide open for local dev / a simple personal project — there's no login
# and no private data here, so nothing sensitive to protect. If you add
# user accounts or real data later, lock this down to your frontend's URL.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/job-descriptions")
def list_job_descriptions():
    """Return the bundled sample job descriptions so the UI can offer them as presets."""
    if not JD_FOLDER.exists():
        return []

    descriptions = []
    for file in sorted(JD_FOLDER.iterdir()):
        if file.is_file() and file.suffix.lower() == ".txt":
            descriptions.append(
                {
                    "id": file.stem,
                    "title": file.stem.replace("_", " ").title(),
                    "content": file.read_text(encoding="utf-8", errors="ignore"),
                }
            )
    return descriptions


@app.post("/api/screen")
async def screen_resumes(
    job_description: str = Form(...),
    resumes: list[UploadFile] = File(...),
):
    """
    Accepts a job description (raw text) and one or more resume files
    (.pdf / .docx), runs each resume through the existing
    read -> parse -> match pipeline, and returns results ranked by score.
    """
    job_description = job_description.strip()
    if not job_description:
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    if not resumes:
        raise HTTPException(status_code=400, detail="Upload at least one resume.")

    for f in resumes:
        suffix = Path(f.filename or "").suffix.lower()
        if suffix not in ALLOWED_SUFFIXES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type '{suffix or 'unknown'}' for '{f.filename}'. "
                "Only .pdf and .docx are supported.",
            )

    try:
        job = parse_job_description(job_description)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Failed to parse job description: {exc}") from exc

    results = []
    errors = []

    with tempfile.TemporaryDirectory() as tmp_dir:
        for upload in resumes:
            suffix = Path(upload.filename).suffix.lower()
            temp_path = Path(tmp_dir) / f"{uuid.uuid4().hex}{suffix}"

            try:
                with temp_path.open("wb") as out:
                    shutil.copyfileobj(upload.file, out)

                resume_text = read_resume(temp_path)
                if not resume_text.strip():
                    raise ValueError("No extractable text found in file.")

                resume = parse_resume(resume_text)
                match = match_resume(job, resume)

                results.append(
                    {
                        "id": uuid.uuid4().hex,
                        "filename": upload.filename,
                        "name": resume.name,
                        "email": resume.email,
                        "education": resume.education,
                        "years_of_experience": resume.years_of_experience,
                        "skills": resume.skills,
                        "projects": resume.projects,
                        "score": match.get("score", 0),
                        "matched_skills": match.get("matched_skills", []),
                        "missing_skills": match.get("missing_skills", []),
                        "summary": match.get("summary", ""),
                    }
                )
            except Exception as exc:
                errors.append({"filename": upload.filename, "error": str(exc)})
            finally:
                upload.file.close()

    results.sort(key=lambda r: r["score"], reverse=True)

    return {
        "job": job.model_dump(),
        "results": results,
        "errors": errors,
    }
