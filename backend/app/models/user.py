from pydantic import BaseModel

class User(BaseModel):
    _id: str
    name: str
    age: int
