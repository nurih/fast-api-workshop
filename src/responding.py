from enum import Enum
import pathlib
from fastapi import Body, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
import uvicorn


class Stooge(Enum):
    Larry = 1
    Moe = 2
    Curly = 3


api = FastAPI(swagger_ui_parameters={'tryItOutEnabled': True})


@api.get('/response/json')
async def respond_json():
    """Call me to get JSON response with text/json media type"""
    return JSONResponse(content={"greeting": "Hi", "s": Stooge.Moe.name},
                        status_code=status.HTTP_226_IM_USED, )


@api.get('/response/file')
async def respond_file():
    """
    Call me to get a file response with media 
    type guessed from file or explicitly set through `media_type`
    """
    return FileResponse(r'docs\img\capybara_squirrel_monkey.jpg')


@api.get('/response/html')
async def respond_html():
    """Call me to get HTML content as a response"""
    return HTMLResponse("""
    <html>
        <head>
            <title>Great Page</title>
        </head>
        <body>
            <h1>Hi</h1>
            <p>Lorem ipsum dolor <blink>sit</blink> amet.</p>
        </body>
    </html>
    """)

db = MongoClient('mongodb://localhost/test').get_default_database('test')
db.stooges.delete_many({})


class Stooge(Enum):
    Larry = 1
    Moe = 2
    Curly = 3


async def my_handling(request, err: DuplicateKeyError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": f"Document already exists. {str(err)}"},
    )


api.add_exception_handler(DuplicateKeyError, handler=my_handling)


@api.get('/boom/1')
async def boom1():
    """Uncaught server side exceptions become an HTTP 500 response"""
    return 1/0

@api.get('/boom/2')
async def boom2():
    """Specific exception status can be controlled via raising HTTP Exception"""
    raise HTTPException(
        status_code=status.HTTP_421_MISDIRECTED_REQUEST,
        detail="Wrong number!")


@api.post('/boom')
async def create(stooge: Stooge = Body()):
    db.stooges.insert_one({'_id': stooge.value, 'name': stooge.name})
    return list(db.stooges.find())


# Manual entry point
if __name__ == '__main__':
    """Entry point to activate uvicorn"""
    uvicorn.run(f"{pathlib.Path(__file__).stem}:api", reload=True)
