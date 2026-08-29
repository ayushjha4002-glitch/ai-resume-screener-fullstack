from pydantic import BaseModel, Field

class JobD(BaseModel):
    role: str
    required_skills: list[str]
    years_of_experience: float | None = None
    education: str | None = None
    other_requirements: list[str] = Field(default_factory=list)


class Resume(BaseModel):
    name: str
    email: str
    skills: list[str]
    years_of_experience: float | None = None
    education: str | None = None
    projects: list[str] = Field(default_factory=list)