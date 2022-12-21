from enum import Enum
import pathlib
from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn

my_behavior = {
    'tryItOutEnabled': True,
    # 'docExpansion': 'full'
}

api = FastAPI(
    swagger_ui_parameters=my_behavior,
    docs_url='/d/swagger',
    redoc_url='/d/redoc',
    description="""
## Fun Starts Here!

- Yip
- Yup
- Yap

----

### ... And never ends

> The following is about the function `doSomething(s:thing)`

var|desc
---|---
`foo`| The fooness of things
`bar`| The place around the corner

"""
)


class Tags(Enum):
    marklar = "Marklar"
    smurf = "Smurf"


@api.get("/", tags=[Tags.marklar])
async def root(): return {'ack': True}


@api.get("/meta/a", tags=[Tags.marklar])
async def open_api_a(): return {'ack': 'a'}
@api.get("/meta/b", tags=[Tags.smurf])
async def open_api_b(): return {'ack': 'b'}
@api.get("/meta/c", tags=[Tags.marklar])
async def open_api_c(): return {'ack': 'c'}


@api.get('/meta/route_decore',
         summary='My Getter',
         description='''My description of my getter.
         
         It has multiple lines
         Like, here is another...
         ''')
async def open_api_d():
    return {'ack': 'd'}


class Thing(BaseModel):
    """
    This thing documents the model - a docstrig.
    """
    name: str = Field(
        title='My field title', 
        description='My field description')


@api.get('/meta/model_decore')
async def open_api_e(thing: Thing): return thing


# Manual entry point
if __name__ == '__main__':
    """Entry point to activate uvicorn"""
    uvicorn.run(f"{pathlib.Path(__file__).stem}:api",
                host="0.0.0.0", port=8000, reload=True)


