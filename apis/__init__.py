from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=[""],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def root():
    return {'Hello': '"반려동물 감정 및 상황 해석을 위한 울음 감지 및 분석 어플리케이션" 프로젝트의 Backend Repository입니다.'}
