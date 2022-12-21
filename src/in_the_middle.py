import os
import uvicorn
from fastapi import FastAPI, Request
from db import DB
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware

db = DB(os.environ['MONGO_URL'])


class YeetMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers['Custom'] = 'yeet!'
        return response


api = FastAPI(middleware=[Middleware(YeetMiddleware)])

@api.get("/api")
async def root():
    return {"message": "Hello, it depends"}


if __name__ == '__main__':
    uvicorn.run("in_the_middle:api", host="127.0.0.1", port=8000, reload=True)
