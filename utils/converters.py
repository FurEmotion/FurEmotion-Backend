# utils/converters.py
from model.user import UserTable
from model.pet import PetTable
from model.cry import CryTable

from schemas.user import User
from schemas.pet import Pet
from schemas.cry import Cry


def user_table_to_schema(user_table: UserTable) -> User:
    pets = [pet_table_to_schema(pet)
            for pet in user_table.pets] if user_table.pets else []
    return User(
        uid=user_table.uid,
        email=user_table.email,
        nickname=user_table.nickname,
        photoId=user_table.photoId,
        pets=pets
    )


def pet_table_to_schema(pet_table: PetTable) -> Pet:
    cries = [cry_table_to_schema(cry)
             for cry in pet_table.cries] if pet_table.cries else []
    return Pet(
        id=pet_table.id,
        name=pet_table.name,
        gender=pet_table.gender,
        age=pet_table.age,
        species=pet_table.species,
        sub_species=pet_table.sub_species,
        user_id=pet_table.user_id,
        photo_id=pet_table.photo_id,
        cries=cries
    )


def cry_table_to_schema(cry_table: CryTable) -> Cry:
    return Cry(
        id=cry_table.id,
        pet_id=cry_table.pet_id,
        time=cry_table.time,
        state=cry_table.state,
        audioId=cry_table.audioId,
        predictMap=cry_table.predictMap,
        intensity=cry_table.intensity,
        duration=cry_table.duration
    )
