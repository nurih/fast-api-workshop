from enum import Enum
from fastapi import FastAPI, HTTPException, Query, status
import uvicorn

api = FastAPI()


@api.get("/")
async def root():
    return "Hi."


@api.get("/even/{number}",)
async def get_even(number: int):
    return {
        "number": number,
        'ok': number % 2 == 0
    }


@api.get("/add/{a}/{b}")
async def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "sum": a+b
    }


@api.get("/div/")
async def divide(a: int = Query(title='number'), b: int = Query(title="divisor", gt=0)) -> float:
    return {'result': a/b}


class MathOperator(str, Enum):
    add = 'add'
    div = 'div'
    mult = 'mult'
    sub = 'sub'

    def exec(self, a, b):
        f = {
            'add': lambda x, y: x+y,
            'div': lambda x, y: x/y,
            'mult': lambda x, y: x*y,
            'sub': lambda x, y: y-x
        }[self.value]
        return f(a, b)


@api.get("/calc/{op}")
async def calc(a: int, b: int, op: MathOperator):
    try:
        return {'op': 'op',  'result': op.exec(a, b)}
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail='Dude, really?!')


# Manual entry point
if __name__ == '__main__':
    """Entry point to activate uvicorn"""
    uvicorn.run("pathings:api", host="127.0.0.1", port=8000, reload=True)
