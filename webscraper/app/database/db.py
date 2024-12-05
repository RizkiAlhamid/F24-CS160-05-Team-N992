from motor.motor_asyncio import AsyncIOMotorClient
from app.lib.credentials import MONGO_URI

# MongoDB connection
client = AsyncIOMotorClient(MONGO_URI)

database = client.my_database

async def check_connection():
    try:
        # Perform the ping command
        await client.admin.command('ping')
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
