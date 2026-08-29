import os
from config import RESUME_FOLDER
from matcher import match_resume
from parser import parse_job_description, parse_resume
from reader import read_resume

jd_folder = "job_descriptions"

jd_files = os.listdir(jd_folder)

print("\nAvailable Job Descriptions:\n")

for i, file in enumerate(jd_files, start=1):
    print(f"{i}. {file}")

choice = int(input("\nEnter your choice: "))

selected_file = jd_files[choice - 1]

print(f"\nSelected Job Description: {selected_file}")

JOB_DESCRIPTION = """
We are hiring a Backend Python Developer.

Requirements:
- Python
- FastAPI
- SQL
- Docker

Experience:
2 years

Education:
B.Tech
"""

job = parse_job_description(JOB_DESCRIPTION)

resume_files = [
    file
    for file in RESUME_FOLDER.iterdir()
    if file.is_file() and file.suffix.lower() in [".pdf", ".docx"]
]

for file in resume_files:
   


    resume_text = read_resume(file)

    resume = parse_resume(resume_text)

    result = match_resume(job, resume)

    print("=" * 60)
    print("Candidate :", resume.name)
    print("Score     :", result["score"])
    print("Summary   :", result["summary"])
    print("=" * 60)
