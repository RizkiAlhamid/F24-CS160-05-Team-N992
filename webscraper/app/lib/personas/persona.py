from app.database.db import database

collection = database.personas

def get_all_personas():
    return collection.find()

def get_persona_by_id(str_id: str):
    return collection.find_one({"id": str_id})

def create_persona(persona: dict):
    return collection.insert_one(persona)
