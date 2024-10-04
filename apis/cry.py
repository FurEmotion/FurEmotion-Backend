# apis/cry.py
from fastapi import APIRouter, HTTPException, Depends, Query
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR)
from sqlalchemy.orm import Session
import logging
from typing import Optional
from datetime import datetime

from auth.auth_bearer import JWTBearer
from services.cry import cry_service
from schemas.cry import *
from db import get_db_session
from error.exceptions import *

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/cry",
    tags=["cry"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", dependencies=[Depends(JWTBearer())], response_model=CreateCryOutput)
def create_cry_endpoint(
        create_cry_input: CreateCryInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> CreateCryOutput:
    try:
        cry = cry_service.create_cry(db, create_cry_input, user_id)
        cry.to_korean()

        return CreateCryOutput(cry=cry, success=True, message="Cry created successfully")

    except (ValidationError, UnauthorizedError) as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception(f"Unexpected error in create_cry API: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


@router.get("/cry/{cry_id}", dependencies=[Depends(JWTBearer())], response_model=GetCryOutput)
def get_cry_endpoint(
        cry_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetCryOutput:
    try:
        cry = cry_service.get_cry_by_id(db, cry_id, user_id)
        cry.to_korean()
        return GetCryOutput(cry=cry, success=True, message="Cry fetched successfully")
    except CryNotFoundError as cnfe:
        logger.error(f"Cry not found: {cnfe}")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(cnfe))
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception(f"Unexpected error in get_cry API: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


@router.get("/pet/{pet_id}", dependencies=[Depends(JWTBearer())], response_model=GetPetCriesOutput)
def get_pet_cries_endpoint(
        pet_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetPetCriesOutput:
    try:
        cries = cry_service.get_all_cries_by_pet(db, pet_id, user_id)
        for cry in cries:
            cry.to_korean()
        return GetPetCriesOutput(cries=cries, success=True, message="Cries fetched successfully")
    except UnauthorizedError as ue:
        logger.error(f"Unauthorized access: {ue}")
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(ue))
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception(f"Unexpected error in get_pet_cries API: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


@router.put("/{cry_id}", dependencies=[Depends(JWTBearer())], response_model=UpdateCryOutput)
def update_cry_endpoint(
        cry_id: int,
        update_cry_input: UpdateCryInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> UpdateCryOutput:
    try:
        cry = cry_service.update_cry(db, cry_id, update_cry_input, user_id)
        cry.to_korean()
        return UpdateCryOutput(cry=cry, success=True, message="Cry updated successfully")
    except CryNotFoundError as cnfe:
        logger.error(f"Cry not found: {cnfe}")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(cnfe))
    except (ValidationError) as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception(f"Unexpected error in update_cry API: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


@router.delete("/{cry_id}", dependencies=[Depends(JWTBearer())], response_model=DeleteCryOutput)
def delete_cry_endpoint(
        cry_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> DeleteCryOutput:
    try:
        cry_service.delete_cry(db, cry_id, user_id)
        return DeleteCryOutput(success=True, message="Cry deleted successfully")
    except CryNotFoundError as cnfe:
        logger.error(f"Cry not found: {cnfe}")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(cnfe))
    except (ValidationError) as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception(f"Unexpected error in delete_cry API: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


@router.get("/search/state", dependencies=[Depends(JWTBearer())], response_model=GetPetsWithStateOutput)
def get_pets_with_state_endpoint(
        pet_id: int = Query(..., description="ID of the pet"),
        query_state: str = Query(..., description="State to filter cries"),
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetPetsWithStateOutput:
    try:
        cries = cry_service.get_pets_with_state(
            db, pet_id, query_state, user_id)
        for cry in cries:
            cry.to_korean()
        return GetPetsWithStateOutput(pets=cries, success=True, message="Cries fetched successfully")
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception(f"Unexpected error in get_pets_with_state API: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


@router.get("/search/time", dependencies=[Depends(JWTBearer())], response_model=GetPetsBetweenTimeOutput)
def get_pets_between_time_endpoint(
        pet_id: int = Query(..., description="ID of the pet"),
        start_time: datetime = Query(...,
                                     description="Start time in ISO format"),
        end_time: datetime = Query(..., description="End time in ISO format"),
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetPetsBetweenTimeOutput:
    try:
        cries = cry_service.get_pets_between_time(
            db, pet_id, start_time, end_time, user_id)
        for cry in cries:
            cry.to_korean()
        return GetPetsBetweenTimeOutput(pets=cries, success=True, message="Cries fetched successfully")
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception(f"Unexpected error in get_pets_between_time API: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )
