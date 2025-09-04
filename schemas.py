from pydantic import BaseModel, HttpUrl, field_validator, EmailStr, constr
from typing import List
import re

# Nested model for Projects
class Project(BaseModel):
    name: str
    desc: str
    link: HttpUrl

    @field_validator("name", "desc")
    def non_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Fields cannot be empty")
        return v.strip()

# Nested model for Work Experience
class WorkExperience(BaseModel):
    role: str
    company: str
    duration: str
    details: str

    @field_validator("role", "company", "duration", "details")
    def non_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Experience fields cannot be empty")
        return v.strip()

# Main Profile model
class ProfileCreate(BaseModel):
    name: str
    email: EmailStr
    phone: constr(strip_whitespace=True)  # regex validation below
    education: str
    skills: List[str]
    projects: List[Project]
    work_experience: List[WorkExperience]

    # Name validation
    @field_validator("name")
    def name_must_be_valid(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty")
        if not v.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters and spaces")
        return v.title()

    # Phone number validation
    @field_validator("phone")
    def validate_phone(cls, v):
        # Only +91XXXXXXXXXX or 10 digits
        pattern = re.compile(r"^(?:\+91\d{10}|\d{10})$")
        if not pattern.match(v):
            raise ValueError("Invalid phone number format. Use +91XXXXXXXXXX or 10 digits")
        return v

    # Education validation
    @field_validator("education")
    def validate_education(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Education field cannot be empty")
        return v.strip()

    # Skills validation
    @field_validator("skills")
    def validate_skills(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("At least one skill is required")
        if any(not skill.strip() for skill in v):
            raise ValueError("Skill entries cannot be empty")
        return [s.strip() for s in v]
