from fastapi import APIRouter, UploadFile, HTTPException, Depends, File, Header, Form
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer

from services.user import UserService
from schemas.user import *


router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

userService = UserService()


# @router.post("/")
# def create_user(createUserInput: CreateUserInput) -> CreateUserOutput:
#     try:
#         user = userService.create_user(createUserInput)
#     except Exception as e:
#         raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
