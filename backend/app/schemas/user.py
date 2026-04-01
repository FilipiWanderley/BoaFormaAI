from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)
    age: int = Field(gt=0, lt=120)
    weight_kg: float = Field(gt=0)
    height_cm: float = Field(gt=0)
    goal: str = Field(min_length=3, max_length=50)
    level: Literal["iniciante", "intermediario", "avancado"]
    restrictions: Optional[str] = Field(default=None, max_length=500)
    accept_terms: Literal[True]
    privacy_policy_version: str = Field(default="2026-01", min_length=3, max_length=20)

    @field_validator("name")
    @classmethod
    def name_must_have_surname(cls, v: str) -> str:
        if len(v.split()) < 2:
            raise ValueError("Informe nome e sobrenome")
        return v.strip()


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    weight_kg: float
    height_cm: float
    goal: str
    level: str
    restrictions: Optional[str]
    provider: str
    provider_id: Optional[str]
    is_admin: bool
    consent_given_at: Optional[datetime]
    privacy_policy_version: Optional[str]
    avatar_url: Optional[str]

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    weight_kg: Optional[float] = Field(default=None, gt=0)
    height_cm: Optional[float] = Field(default=None, gt=0)
    goal: Optional[str] = Field(default=None, min_length=3, max_length=50)
    restrictions: Optional[str] = None
    avatar_url: Optional[str] = Field(default=None, max_length=4_500_000)
