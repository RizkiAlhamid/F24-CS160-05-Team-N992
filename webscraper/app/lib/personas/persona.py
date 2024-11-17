from app.database.db import database

collection = database.personas

async def get_all_personas():
    return await collection.find().to_list(length=None)

async def get_first_persona():
    personas = await get_all_personas()
    if personas:
        return personas[0]  # Return the first persona
    return None

def get_persona_by_id(str_id: str):
    return collection.find_one({"id": str_id})

def create_persona(persona: dict):
    return collection.insert_one(persona)
