from models import JobD, Resume

JOB_DESCRIPTION_PROMPT = f"""
You are an expert recruitment assistant.

Extract the following information from the given job description.

Return ONLY a valid JSON object matching this schema.

Schema:
{JobD.model_json_schema()}
"""
RESUME_PROMPT = f"""
You are an expert resume parser.

Extract the candidate information.

Return ONLY a valid JSON object matching this schema.

Schema:
{Resume.model_json_schema()}
"""
