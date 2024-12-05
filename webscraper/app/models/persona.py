from pydantic import BaseModel
from typing import List

class Background(BaseModel):
    history: str
    motivation: str

class Persona(BaseModel):
    id: str
    name: str
    species: str
    residence: str
    occupation: str
    personality: dict
    background: Background
    goals: dict
    segments: dict
    signature_lines: List[str]
    engagement_tactics: dict

class Personas(BaseModel):
    personas: List[Persona]
