# apis/pet.py
from fastapi import APIRouter, HTTPException, Depends
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR)
from sqlalchemy.orm import Session

from auth.auth_bearer import JWTBearer
from services.pet import pet_service
from schemas.pet import *
from db import get_db_session
from error.exceptions import *

router = APIRouter(
    prefix="/pet",
    tags=["pet"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", dependencies=[Depends(JWTBearer())], response_model=CreatePetOutput)
def create_pet_endpoint(
        create_pet_input: CreatePetInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> CreatePetOutput:
    try:
        pet = pet_service.create_pet(db, create_pet_input, user_id)
        pet.to_korean()

        return CreatePetOutput(pet=pet, success=True, message="Pet created successfully")

    except (ValidationError, NegativeAgeError, InvalidSpeciesError) as ve:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


@router.get("/{pet_id}", dependencies=[Depends(JWTBearer())], response_model=GetPetOutput)
def get_pet_endpoint(
        pet_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetPetOutput:
    try:
        pet = pet_service.get_pet_by_id(db, pet_id, user_id)
        pet.to_korean()
        return GetPetOutput(pet=pet, success=True, message="Pet fetched successfully")
    except PetNotFoundError as pnfe:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(pnfe))
    except ValidationError as ve:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


@router.get("/user/{user_id}", dependencies=[Depends(JWTBearer())], response_model=GetUserPetsOutput)
def get_user_pets_endpoint(
        user_id: str,
        db: Session = Depends(get_db_session),
        requester_id: str = Depends(JWTBearer())) -> GetUserPetsOutput:
    try:
        if user_id != requester_id:
            raise UnauthorizedError(
                "You are not authorized to view these pets")

        pets = pet_service.get_all_pets_by_user(db, user_id)
        for pet in pets:
            pet.to_korean()

        return GetUserPetsOutput(pets=pets, success=True, message="Pets fetched successfully")
    except UnauthorizedError as ue:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(ue))
    except ValidationError as ve:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


@router.put("/{pet_id}", dependencies=[Depends(JWTBearer())], response_model=UpdatePetOutput)
def update_pet_endpoint(
        pet_id: int,
        update_pet_input: UpdatePetInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> UpdatePetOutput:
    try:
        pet = pet_service.update_pet(db, pet_id, update_pet_input, user_id)
        pet.to_korean()
        return UpdatePetOutput(pet=pet, success=True, message="Pet updated successfully")
    except PetNotFoundError as pnfe:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(pnfe))
    except (ValidationError, NegativeAgeError, InvalidSpeciesError) as ve:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


@router.delete("/{pet_id}", dependencies=[Depends(JWTBearer())], response_model=DeletePetOutput)
def delete_pet_endpoint(
        pet_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> DeletePetOutput:
    try:
        pet_service.delete_pet(db, pet_id, user_id)
        return DeletePetOutput(success=True, message="Pet deleted successfully")
    except PetNotFoundError as pnfe:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(pnfe))
    except ValidationError as ve:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )
