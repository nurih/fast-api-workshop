import uvicorn
from fastapi import FastAPI
import area1.main as area1
import area51.main as area51


api = FastAPI()

api.include_router(area1.router)
api.include_router(area51.router)

@api.get("/")
async def root():
    return {"message": "Hello bigger app"}


if __name__ == '__main__':
    uvicorn.run("main:api", host="127.0.0.1", port=8000, reload=True)
