from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=[""],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def root():
    return {'hello': 'world'}
