from fastapi import FastAPI

api = FastAPI()


@api.get("/")
async def root():
    return "Hello Fast API"


@api.get("/hello")
async def greeting():
    return "Hello hello"
