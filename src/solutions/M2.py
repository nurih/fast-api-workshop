
from enum import Enum
import pathlib
from typing import Optional
from fastapi import FastAPI, Query, Path
import uvicorn

api = FastAPI()


@api.post("/order1/")
async def create_order1(item: str, quantity: int):
    return {'item': item, 'quantity': quantity}


@api.post("/order2/")
async def create_order2(item: str, quantity: Optional[int] = 1):
    return {'item': item, 'quantity': quantity}


@api.post("/order3/")
async def create_order3(item: str = Query(title='Item', regex=r'^[A-Z][A-Z0-9]{2}$'), quantity: Optional[int] = 1):
    return {'item': item, 'quantity': quantity}


@api.patch("/order3/{id}")
async def create_order3(*, id: int = Path(title='Item id', gt=0), fields: dict[str, str]):
    return {'id': id, 'updated_fields': fields}


class LetterSize(Enum):
    S = 'S'
    M = 'M'
    L = 'L'
    XL = 'XL'
    G = 'Gigantic'


@api.get('/order4/{size}')
async def list_orders(size: LetterSize):
    return {'item': 'Shirt', 'size': size}

# Manual entry point
if __name__ == '__main__':
    """Entry point to activate uvicorn"""
    uvicorn.run(f"{pathlib.Path(__file__).stem}:api",
                host="127.0.0.1", port=8000, reload=True)
