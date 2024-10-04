# apis/user.py
from fastapi import APIRouter, HTTPException, Depends
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR)
from sqlalchemy.orm import Session
import logging
from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT
from services.user import UserService
from schemas.user import *
from db import get_db_session
from error.exceptions import *

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

user_service = UserService()


@router.post("/me", response_model=CreateUserOutput)
def create_user_endpoint(
        create_user_input: CreateUserInput,
        db: Session = Depends(get_db_session)) -> CreateUserOutput:
    try:
        user = user_service.create_user(db, create_user_input)
        jwt_token = signJWT(user.uid)
        return CreateUserOutput(user=user, token=jwt_token, success=True, message="User created successfully")
    except DuplicateEmailError as dee:
        logger.error(f"Duplicate email error: {dee}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(dee))
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception(f"Unexpected error in create_user API: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


@router.get("/me", dependencies=[Depends(JWTBearer())], response_model=GetUserOutput)
def get_current_user_endpoint(
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetUserOutput:
    try:
        user = user_service.get_user_by_id(db, user_id)
        return GetUserOutput(user=user, success=True, message="User fetched successfully")
    except UserNotFoundError as unfe:
        logger.error(f"User not found: {unfe}")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(unfe))
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception(f"Unexpected error in get_user_by_id API: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@ router.put("/me", dependencies=[Depends(JWTBearer())], response_model=UpdateUserOutput)
def update_user_endpoint(
        update_user_input: UpdateUserInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> UpdateUserOutput:
    try:
        user = user_service.update_user(db, user_id, update_user_input)
        return UpdateUserOutput(user=user, success=True, message="User updated successfully")
    except DuplicateEmailError as dee:
        logger.error(f"Duplicate email error: {dee}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(dee))
    except UserNotFoundError as unfe:
        logger.error(f"User not found: {unfe}")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(unfe))
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception(f"Unexpected error in update_user API: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


@ router.delete("/me", dependencies=[Depends(JWTBearer())], response_model=DeleteUserOutput)
def delete_user_endpoint(
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> DeleteUserOutput:
    try:
        user_service.delete_user(db, user_id)
        return DeleteUserOutput(success=True, message="User deleted successfully")
    except UserNotFoundError as unfe:
        logger.error(f"User not found: {unfe}")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(unfe))
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception(f"Unexpected error in delete_user API: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


@ router.get("/user/{target_user_id}", dependencies=[Depends(JWTBearer())], response_model=GetUserOutput)
def get_user_by_id_endpoint(
        target_user_id: str,
        db: Session = Depends(get_db_session),
        requester_id: str = Depends(JWTBearer())) -> GetUserOutput:
    try:
        user = user_service.get_user_by_id(db, target_user_id)
        return GetUserOutput(user=user, success=True, message="User fetched successfully")
    except UserNotFoundError as unfe:
        logger.error(f"User not found: {unfe}")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(unfe))
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception(f"Unexpected error in get_user_by_id API: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@ router.post("/me/login", response_model=LoginUserOutput)
def login(
        login_user_input: LoginUserInput,
        db: Session = Depends(get_db_session)) -> LoginUserOutput:
    try:
        user = user_service.login(db, login_user_input)
        jwt_token = signJWT(user.uid)
        return LoginUserOutput(user=user, token=jwt_token, success=True, message="User logged in successfully")
    except UserNotFoundError as unfe:
        logger.error(f"User not found: {unfe}")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(unfe))
    except UnauthorizedError as ue:
        logger.error(f"Unauthorized access: {ue}")
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(ue))
    except Exception as e:
        logger.exception(f"Unexpected error in login API: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )
