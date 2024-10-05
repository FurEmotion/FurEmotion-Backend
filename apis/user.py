from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT
from services.user import user_service
from schemas.user import *
from db import get_db_session
from error.exceptions import *
from error.handler import handle_http_exceptions

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.post("/me", response_model=CreateUserOutput)
@handle_http_exceptions
def create_user_endpoint(
        create_user_input: CreateUserInput,
        db: Session = Depends(get_db_session)) -> CreateUserOutput:
    user = user_service.create_user(db, create_user_input).to_korean()
    jwt_token = signJWT(user.uid)
    return CreateUserOutput(user=user, token=jwt_token, success=True, message="User created successfully")


@router.get("/me", dependencies=[Depends(JWTBearer())], response_model=GetUserOutput)
@handle_http_exceptions
def get_current_user_endpoint(
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetUserOutput:
    user = user_service.get_user_by_id(db, user_id).to_korean()
    return GetUserOutput(user=user, success=True, message="User fetched successfully")


@router.put("/me", dependencies=[Depends(JWTBearer())], response_model=UpdateUserOutput)
@handle_http_exceptions
def update_user_endpoint(
        update_user_input: UpdateUserInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> UpdateUserOutput:
    user = user_service.update_user(db, user_id, update_user_input).to_korean()
    return UpdateUserOutput(user=user, success=True, message="User updated successfully")


@router.delete("/me", dependencies=[Depends(JWTBearer())], response_model=DeleteUserOutput)
@handle_http_exceptions
def delete_user_endpoint(
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> DeleteUserOutput:
    user_service.delete_user(db, user_id)
    return DeleteUserOutput(success=True, message="User deleted successfully")


@router.get("/user/{target_user_id}", dependencies=[Depends(JWTBearer())], response_model=GetUserOutput)
@handle_http_exceptions
def get_user_by_id_endpoint(
        target_user_id: str,
        db: Session = Depends(get_db_session),
        requester_id: str = Depends(JWTBearer())) -> GetUserOutput:
    user = user_service.get_user_by_id(db, target_user_id).to_korean()
    return GetUserOutput(user=user, success=True, message="User fetched successfully")


@router.post("/me/login", response_model=LoginUserOutput)
@handle_http_exceptions
def login(
        login_user_input: LoginUserInput,
        db: Session = Depends(get_db_session)) -> LoginUserOutput:
    user = user_service.login(db, login_user_input).to_korean()
    jwt_token = signJWT(user.uid)
    return LoginUserOutput(user=user, token=jwt_token, success=True, message="User logged in successfully")
