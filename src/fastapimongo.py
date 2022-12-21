from pydantic import BaseModel
from pymongo import MongoClient
import pathlib
from fastapi import FastAPI
import uvicorn

api = FastAPI()

client = MongoClient('mongodb://localhost/test')
db = client.get_default_database('test')
collection = db['fastapi']

class Customer(BaseModel):
    email: str
    name: str


@api.post('/customer')
async def create(customer:Customer):
    doc = customer.dict()
    doc['_id'] = doc.pop('email')
    collection.insert_one(doc)


@api.get('/customer/{email}', response_model=Customer)
async def get_one(email: str):
    doc = collection.find_one({'_id': email})
    doc['email'] = doc.pop('_id')
    return Customer(**doc)

# Manual entry point
if __name__ == '__main__':
    """Entry point to activate uvicorn"""
    uvicorn.run(f"{pathlib.Path(__file__).stem}:api", reload=True)
