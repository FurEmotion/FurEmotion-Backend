from fastapi import APIRouter, UploadFile, HTTPException, Depends, File, Header, Form
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer

from services.cry import CryService
from schemas.cry import *


router = APIRouter(
    prefix="/cry",
    tags=["cry"],
    responses={404: {"description": "Not found"}},
)

cryService = CryService()
