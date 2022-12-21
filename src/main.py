import os
from typing import List
import uvicorn
from fastapi import FastAPI
from models import Person
from db import DB
# from async_db import AsyncDB
# from src.simplistic import TransparentIdHandler
# from pydanticmongo.pydanticmongo import TransparentIdHandler

# from pydantic import BaseModel
# from starlette.routing import request_response

api = FastAPI()

db = DB(os.environ['MONGO_URL'])

# db = AsyncDB(os.environ['MONGO_URL'], id_handler=TransparentIdHandler( default_factory= lambda: 0))


@api.get("/")
async def root():
    return {"message": "Hello World"}


@api.get("/fish/{named}")
async def get_thing_named(named: str):
    return {'name': named, 'text': "~~   >-+``+,,)°>   ~"}


@api.get("/files/{extra_after_whatever_before:path}")
async def read_file(extra_after_whatever_before: str):
    return {
        "extra": extra_after_whatever_before,
        "text": "Got a request to read this file. I dunno... maybe I will."
    }


@api.get('/peeps/{_id}')
async def get_person(_id: Person.id) -> List[Person]:
    return await db.get_by_id(_id)


@api.get('/peeps')
async def list_peeps() -> List[Person]:
    return await db.get_all()


@api.put('/peeps')
async def upsert_person(p: Person):
    return await db.create_one(p)


@api.post('/peeps')
async def create():
    await db.prepare_collection()

# Nothing to see here.
# JK: define  start entry point to activate uvicorn via poetry's "start" script hook


def entry():
    """Entry point to activate uvicorn"""
    uvicorn.run("main:api", host="0.0.0.0", port=8000, reload=True)


if __name__ == '__main__':
    entry()
