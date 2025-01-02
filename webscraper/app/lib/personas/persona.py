from app.database.db import database
from bson import ObjectId
from app.lib.logging import logging

collection = database.personas

async def get_all_personas():
    personas = []
    async for persona in collection.find():
        persona["_id"] = str(persona["_id"])  
        personas.append(persona)
    return personas

async def get_first_persona():
    personas = await get_all_personas()
    if personas:
        return personas[0]  # Return the first persona
    return None

async def get_persona_by_id(persona_id: str):
    persona = None
    try:
        # Finding using '_id' identifier
        if ObjectId.is_valid(persona_id):
            persona = await collection.find_one({"_id": ObjectId(persona_id)})
            # Finding using custom 'id', which is the persona's name
        else:
            persona = await collection.find_one({"id": persona_id})
    except Exception as e:
        logging.error(f"Error fetching persona: {e}")

    if not persona:
        logging.error(f"Persona not found: {persona_id}")
        return

    # Convert '_id' to string for JSON serialization
    persona["_id"] = str(persona["_id"])
    return persona

def create_persona(persona: dict):
    return collection.insert_one(persona)
