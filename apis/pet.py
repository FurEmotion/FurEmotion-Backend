# apis/pet.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.auth_bearer import JWTBearer
from services.pet import pet_service
from schemas.pet import *
from db import get_db_session
from error.exceptions import *
from error.handler import handle_http_exceptions

router = APIRouter(
    prefix="/pet",
    tags=["pet"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", dependencies=[Depends(JWTBearer())], response_model=CreatePetOutput)
@handle_http_exceptions
def create_pet_endpoint(
        create_pet_input: CreatePetInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> CreatePetOutput:
    pet = pet_service.create_pet(db, create_pet_input, user_id).to_korean()
    return CreatePetOutput(pet=pet, success=True, message="Pet created successfully")


@router.get("/{pet_id}", dependencies=[Depends(JWTBearer())], response_model=GetPetOutput)
@handle_http_exceptions
def get_pet_endpoint(
        pet_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetPetOutput:
    pet = pet_service.get_pet_by_id(db, pet_id, user_id).to_korean()
    return GetPetOutput(pet=pet, success=True, message="Pet fetched successfully")


@router.get("/user/{user_id}", dependencies=[Depends(JWTBearer())], response_model=GetUserPetsOutput)
@handle_http_exceptions
def get_user_pets_endpoint(
        user_id: str,
        db: Session = Depends(get_db_session),
        requester_id: str = Depends(JWTBearer())) -> GetUserPetsOutput:
    if user_id != requester_id:
        raise UnauthorizedError("You are not authorized to view these pets")

    pets = pet_service.get_all_pets_by_user(db, user_id)
    for i in range(len(pets)):
        pets[i] = pets[i].to_korean()
    return GetUserPetsOutput(pets=pets, success=True, message="Pets fetched successfully")


@router.put("/{pet_id}", dependencies=[Depends(JWTBearer())], response_model=UpdatePetOutput)
@handle_http_exceptions
def update_pet_endpoint(
        pet_id: int,
        update_pet_input: UpdatePetInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> UpdatePetOutput:
    pet = pet_service.update_pet(
        db, pet_id, update_pet_input, user_id).to_korean()
    return UpdatePetOutput(pet=pet, success=True, message="Pet updated successfully")


@router.delete("/{pet_id}", dependencies=[Depends(JWTBearer())], response_model=DeletePetOutput)
@handle_http_exceptions
def delete_pet_endpoint(
        pet_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> DeletePetOutput:
    pet_service.delete_pet(db, pet_id, user_id)
    return DeletePetOutput(success=True, message="Pet deleted successfully")
