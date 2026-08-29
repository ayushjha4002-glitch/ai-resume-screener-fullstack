import json

from config import client, MODEL
from models import JobD, Resume


def match_resume(job: JobD, resume: Resume):
    prompt = f"""
You are an expert technical recruiter.

Compare the following resume with the given job description.

Job Description:
{job.model_dump_json(indent=2)}

Resume:
{resume.model_dump_json(indent=2)}

Return ONLY valid JSON in this format:

{{
    "score": 0-100,
    "matched_skills": [],
    "missing_skills": [],
    "summary": ""
}}
"""

    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
    )

    return json.loads(response.choices[0].message.content)