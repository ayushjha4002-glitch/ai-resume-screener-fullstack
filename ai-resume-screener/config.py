import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY=os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")


client = Groq(api_key=API_KEY)

MODEL= "openai/gpt-oss-120b"
BASE_DIR = Path(__file__).resolve().parent

RESUME_FOLDER = BASE_DIR /"resumes"

