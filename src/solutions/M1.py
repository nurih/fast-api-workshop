from fastapi import FastAPI
import uvicorn
import pathlib

api = FastAPI()


@api.get("/")
async def root():
    return "Hi."


# Manual entry point
if __name__ == '__main__':
    """Entry point to activate uvicorn"""
    uvicorn.run( f"{pathlib.Path(__file__).stem}:api", host="0.0.0.0", port=8000, reload=True)
