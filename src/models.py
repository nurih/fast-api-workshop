from typing import Any, Iterator, Optional
from pydantic import BaseModel
from typing import List, Set, Union
from pydantic.fields import Field
from pydantic.utils import GetterDict


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class User(BaseModel):
    user: str
    password: Optional[str] = None


class Person(BaseModel):
    id: Any = Field(..., alias="_id")
    name: str
