from common import routing

router = routing.get_router_by_folder(__file__)


@router.get("/")
async def function_one():
    return {"message": "Hello from Area One!"}
