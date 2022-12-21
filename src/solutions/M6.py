import pathlib
from pydantic import BaseModel
from pydantic.fields import Field
from fastapi import FastAPI, status, HTTPException
from enum import Enum
import uvicorn
import os
from pymongo.errors import DuplicateKeyError
import motor.motor_asyncio


api = FastAPI()


class Person(BaseModel):
    id: str = Field(title='Email of the person')
    name: str = Field(title='Name of the person')
    GPA: float | None = Field(
        title='Grade point average', ge=.0, le=4.0, default=None)


@api.get("/")
async def root():
    return 'Go to /docs'


class UiGroupingTags(Enum):
    marklar = "Marklar"
    smurf = "Smurf"
    mongo = "mongo"


try:
    mongo_url = os.environ["MONGO_URL"]
    db = motor.motor_asyncio.AsyncIOMotorClient(
        mongo_url).get_default_database()
except Exception as e:
    print('Oh nos!', e)


def modelize(doc):
    doc['id'] = doc.pop('_id')
    return doc


def documentize(model: BaseModel):
    doc = model.dict()
    doc['_id'] = doc.pop('id')
    return doc


@api.get("/people", tags=[UiGroupingTags.mongo], response_model=list[Person])
async def people():
    docs = [modelize(d) async for d in db.people.find({})]
    return docs


@api.get("/people/{id}", tags=[UiGroupingTags.mongo])
async def get_person(id: str):
    doc = await db.people.find_one({'_id': id})

    if doc:
        return modelize(doc)

    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail=f'No match for {id}')


@api.post("/people/", tags=[UiGroupingTags.mongo])
async def add_person(person: Person):
    try:
        return (await db.people.insert_one(documentize(person))).inserted_id
    except DuplicateKeyError:
        raise HTTPException(status.HTTP_409_CONFLICT,
                            detail=f'Attempt to create an already existing entity {person.id}. Did you mean to update?')
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Oh snap!')


# Manual entry point
if __name__ == '__main__':
    """Entry point to activate uvicorn"""
    uvicorn.run(f"{pathlib.Path(__file__).stem}:api",
                host="0.0.0.0", port=8000, reload=True)
