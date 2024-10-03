# apis/pet.py
from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy.orm import Session
import logging

from auth.auth_bearer import JWTBearer
from services.pet import PetService
from schemas.pet import CreatePetInput, CreatePetOutput
from db import get_db_session
from error.exceptions import *

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/pet",
    tags=["pet"],
    responses={404: {"description": "Not found"}},
)

pet_service = PetService()


@router.post("/create", dependencies=[Depends(JWTBearer())], response_model=CreatePetOutput)
def create_pet_endpoint(
        create_pet_input: CreatePetInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> CreatePetOutput:
    try:
        pet = pet_service.create_pet(db, create_pet_input, user_id)
        pet.to_korean_species()

        return CreatePetOutput(pet=pet, success=True, message="Pet created successfully")

    except (ValidationError, NegativeAgeError, InvalidSpeciesError) as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception(f"Unexpected error in create_pet API: {e}")
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )
