from fastapi import HTTPException, APIRouter
from app.main import app
from app.models.user import User 
from app.database.db import database

router = APIRouter()
users_collection = database.get_collection("users")

@app.post("/users")
async def create_user(user: User):
    new_user = await users_collection.insert_one(user.model_dump())
    if new_user.inserted_id:
        return {"message": "User created", "user_id": str(new_user.inserted_id)}
    else:
       raise HTTPException(status_code=400, detail="Error creating user") 

@app.get("/users")
async def get_users():
    users = []
    async for user in users_collection.find():
        user["_id"] = str(user["_id"])
        users.append(User(**user))
    return {"users": users}
