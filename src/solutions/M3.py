from enum import Enum
import pathlib
from typing import List, Optional, Set, Union
from fastapi import FastAPI, Path
from pydantic import BaseModel, Field
import uvicorn

api = FastAPI()


class Superpower(str, Enum):
    strong = 'strong'
    fly = 'fly'
    laser_eyes = 'laser'
    gadgets = 'gadgets'


class Hero(BaseModel):
    name: str = Field(title='Hero name',
                      description='The hero name known to the public')
    civilian_name: str | None = Field(
        title='The secret identity!', regex=r'^(?!(Mrs?|Captain))')
    wears_cape: bool | None = True
    superpowers: Set[Superpower]


heroes = (
    {'name': 'Captain Marvel',  'civilian_name': 'Carol', 'superpowers': {
        Superpower.fly, Superpower.laser_eyes, Superpower.strong}},
    {'name': 'Batman', 'civilian_name': 'Bruce',
        'wears_cape': True, 'superpowers': {Superpower.gadgets}},
    {'name': 'Luke Cage', 'civilian_name': 'Luke',
        'wears_cape': False, 'superpowers': {Superpower.strong}},
    {'name': 'Flaming Carrot',
        'wears_cape': False, 'superpowers': {Superpower.gadgets}},

)


@api.post("/heroes")
async def create_one(hero: Hero):
    return {'ok': hero}


@api.get("/heroes/{offset:int}", response_model=Hero)
async def a_hero(offset: int = Path(ge=0, lt=len(heroes))):
    return heroes[offset]


@api.get("/heroes/plain", response_model=List[Hero])
async def as_is():
    return heroes


@api.get("/heroes/no_empties", response_model=List[Hero], response_model_exclude_unset=True)
async def no_empties():
    return heroes


@api.get("/heroes/trim_the_obvious", response_model=List[Hero], response_model_exclude_defaults=True)
async def trim_the_obvious():
    return heroes


@api.get("/heroes/no_doxing", response_model=List[Hero],
         response_model_exclude=['civilian_name'])
async def no_doxing():
    return heroes


# Manual entry point
if __name__ == '__main__':
    """Entry point to activate uvicorn"""
    uvicorn.run(f"{pathlib.Path(__file__).stem}:api", host="0.0.0.0", port=8000, reload=True)
