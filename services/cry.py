# services/cry.py
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from schemas.cry import *
from model.cry import CryTable
from model.pet import PetTable
from error.exceptions import (
    CryNotFoundError, UnauthorizedError, WrongCryOfSpeciesError)
from utils.converters import cry_table_to_schema
from enums.cry_state import check_right_cry_state


class CryService:
    def _get_user_pet(self, db: Session, pet_id: int, user_id: str) -> Optional[PetTable]:
        return db.query(PetTable).filter(
            PetTable.id == pet_id,
            PetTable.user_id == user_id
        ).first()

    def create_cry(self, db: Session, create_cry_input: CreateCryInput, user_id: str) -> Cry:
        pet = self._get_user_pet(db, create_cry_input.pet_id, user_id)
        if not pet:
            raise UnauthorizedError(
                "You are not authorized to create a cry for this pet")

        notRightSpeciesError = check_right_cry_state(
            pet.species, create_cry_input.state)
        if notRightSpeciesError:
            raise WrongCryOfSpeciesError(notRightSpeciesError)

        cry_table = CryTable(**create_cry_input.model_dump())
        db.add(cry_table)
        db.commit()
        db.refresh(cry_table)

        return cry_table_to_schema(cry_table)

    def get_cry_by_id(self, db: Session, cry_id: int, user_id: str) -> Cry:
        cry_table = db.query(CryTable).join(PetTable).filter(
            CryTable.id == cry_id,
            PetTable.user_id == user_id
        ).first()
        if not cry_table:
            raise CryNotFoundError(f"Cry with id {cry_id} not found")
        return cry_table_to_schema(cry_table)

    def get_all_cries_by_pet(self, db: Session, pet_id: int, user_id: str) -> List[Cry]:
        pet = self._get_user_pet(db, pet_id, user_id)
        if not pet:
            raise UnauthorizedError(
                "You are not authorized to view cries for this pet")

        cry_tables = db.query(CryTable).filter(CryTable.pet_id == pet_id).all()
        return [cry_table_to_schema(cry) for cry in cry_tables]

    def update_cry(self, db: Session, cry_id: int, update_cry_input: UpdateCryInput, user_id: str) -> Cry:
        cry_table = db.query(CryTable).join(PetTable).filter(
            CryTable.id == cry_id,
            PetTable.user_id == user_id
        ).first()
        if not cry_table:
            raise CryNotFoundError(f"Cry with id {cry_id} not found")

        pet = self._get_user_pet(db, cry_table.pet_id, user_id)
        if not pet:
            raise UnauthorizedError(
                "You are not authorized to view cries for this pet")

        notRightSpeciesError = check_right_cry_state(
            pet.species, update_cry_input.state)
        if notRightSpeciesError:
            raise WrongCryOfSpeciesError(notRightSpeciesError)

        cry_table.update(**update_cry_input.model_dump(exclude_unset=True))
        db.commit()
        db.refresh(cry_table)

        return cry_table_to_schema(cry_table)

    def delete_cry(self, db: Session, cry_id: int, user_id: str) -> None:
        cry_table = db.query(CryTable).join(PetTable).filter(
            CryTable.id == cry_id,
            PetTable.user_id == user_id
        ).first()
        if not cry_table:
            raise CryNotFoundError(f"Cry with id {cry_id} not found")

        db.delete(cry_table)
        db.commit()

    def get_pets_with_state(self, db: Session, pet_id: int, query_state: str, user_id: str) -> List[Cry]:
        pet = self._get_user_pet(db, pet_id, user_id)
        if not pet:
            raise UnauthorizedError(
                "You are not authorized to view cries for this pet")

        standardized_state = CRY_STATE_KR_TO_EN.get(query_state, query_state)
        notRightSpeciesError = check_right_cry_state(
            pet.species, standardized_state)
        if notRightSpeciesError:
            raise WrongCryOfSpeciesError(notRightSpeciesError)

        cry_tables = db.query(CryTable).filter(
            CryTable.pet_id == pet_id,
            CryTable.state == standardized_state,
        ).all()
        return [cry_table_to_schema(cry) for cry in cry_tables]

    def get_pets_between_time(self, db: Session, pet_id: int, start_time: datetime, end_time: datetime, user_id: str) -> List[Cry]:
        cry_tables = db.query(CryTable).join(PetTable).filter(
            CryTable.pet_id == pet_id,
            CryTable.time >= start_time,
            CryTable.time <= end_time,
            PetTable.user_id == user_id
        ).all()
        return [cry_table_to_schema(cry) for cry in cry_tables]


cry_service = CryService()
