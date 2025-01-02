from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.models.persona import Personas
from app.main import app
from app.database.db import database

router = APIRouter()

personas_collection = database.get_collection("personas")

@router.post("/personas")
async def create_personas(personas: Personas):
    personas_list = [persona.model_dump() for persona in personas.personas]

    result = await personas_collection.insert_many(personas_list)
    return {
        "ids": [str(inserted_id) for inserted_id in result.inserted_ids],
        "message": "Personas created successfully"
    }

@router.get("/personas")
async def get_all_personas():
    personas = []
    async for persona in personas_collection.find():
        persona["_id"] = str(persona["_id"])  
        personas.append(persona)
    return personas

@router.get("/personas/{persona_id}")
async def get_persona(persona_id: str):
    try:
        # Finding using '_id' identifier
        if ObjectId.is_valid(persona_id):
            persona = await personas_collection.find_one({"_id": ObjectId(persona_id)})
        # Finding using custom 'id', which is the persona's name
        else:
            persona = await personas_collection.find_one({"id": persona_id})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error finding persona: {str(e)}")
    
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")

    # Convert '_id' to string for JSON serialization
    persona["_id"] = str(persona["_id"])
    return persona

