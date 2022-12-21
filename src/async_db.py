from typing import Any
from uuid import UUID
import motor.motor_asyncio
from pydanticmongo import MongoBaseModel, StringAsObjectIdHandler
from bson.objectid import ObjectId

import pydantic 

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str
pydantic.json.ENCODERS_BY_TYPE[UUID] = str


class AsyncDB:
    def __init__(self, mongo_url: str, id_handler = StringAsObjectIdHandler) -> None:
        self.id_handler = id_handler
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            mongo_url, uuidRepresentation = 'standard')
        self.db = self.client.get_default_database('test')
        self.my_collection = self.db.demo

    async def prepare_collection(self):
        await self.my_collection.drop()
        await self.my_collection.insert_one({'_id': 1, 'name': 'bob'})
        await self.my_collection.insert_one({'_id': 2, 'name': 'ogg'})
        await self.my_collection.insert_one({'_id': 3, 'name': 'kim'})

    async def get_by_id(self, id: Any):
        target_value = self.id_handler.from_model_type(id) if self.id_handler else id
        return await self.get_by_filter({"_id": target_value})

    async def get_by_filter(self, filter: dict):
        return await self.my_collection.find_one(filter)

    async def get_all(self):
        return [d async for d in self.my_collection.find({})]

    async def create_one(self, p: MongoBaseModel) -> dict:
        doc = p.mongo_doc()
        await self.my_collection.insert_one(doc)
        return doc
