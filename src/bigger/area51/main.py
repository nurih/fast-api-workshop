from common import routing

router = routing.get_router_by_folder(__file__)


@router.get("/{extra}")
async def function_one(extra: str | None = 'The truth is out there!'):
    return {"message": f"Hello {extra}!"}
