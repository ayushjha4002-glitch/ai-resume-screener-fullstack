import json

from config import client, MODEL
from models import JobD, Resume
from prompts import JOB_DESCRIPTION_PROMPT, RESUME_PROMPT

def parse_job_description(job_text: str) -> JobD:
    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": JOB_DESCRIPTION_PROMPT,
            },
            {
                "role": "user",
                "content": job_text,
            },
        ],
    )

    data = json.loads(response.choices[0].message.content)

    return JobD(**data)

def parse_resume(resume_text: str) -> Resume:
    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": RESUME_PROMPT,
            },
            {
                "role": "user",
                "content": resume_text,
            },
        ],
    )

    data = json.loads(response.choices[0].message.content)

    return Resume(**data)
