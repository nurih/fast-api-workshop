from typing import Any
from uuid import UUID
from pymongo import MongoClient
from simplistic import MongoIdHandler
from bson.objectid import ObjectId

from pydantic import BaseModel
import pydantic 
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str
pydantic.json.ENCODERS_BY_TYPE[UUID] = str


class DB:
    def __init__(self, mongo_url: str) -> None:
        self.client = MongoClient(
            mongo_url, uuidRepresentation = 'standard')
        self.db = self.client.get_default_database('test')
        self.my_collection = self.db.demo

    def prepare_collection(self):
        self.my_collection.drop()
        self.my_collection.insert_one({'_id': 'bob@bob.bob', 'name': 'bob' , 'GPA': 3.9 })
        self.my_collection.insert_one({'_id': 'ogg@ogg.ogg', 'name': 'ogg' , 'GPA': 2.0 })
        self.my_collection.insert_one({'_id': 'kim@kim.kim', 'name': 'kim' , 'GPA': 4.6 })

    def get_by_id(self, id: Any, id_handler: MongoIdHandler):
        target_value = id_handler.from_model_type(id)
        return self.get_by_filter({"_id": target_value})

    def get_one_by_filter(self, filter: dict):
        return self.my_collection.find_one(filter)

    def get_all(self, filter: dict):
        return [d for d in self.my_collection.find(filter)]

    def create_one(self, p: BaseModel, id_handler: MongoIdHandler  ) -> dict:
        doc =  id_handler.to_mongo_dict(p.dict())
        self.my_collection.insert_one(doc)
        return doc
