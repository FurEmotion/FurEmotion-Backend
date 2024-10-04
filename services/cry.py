# services/cry.py
from sqlalchemy.orm import Session
import logging
from datetime import datetime

from schemas.cry import *
from model.cry import CryTable
from model.pet import PetTable
from error.exceptions import (
    ValidationError,
    CryNotFoundError,
    UnauthorizedError,
    PetNotFoundError
)
from utils.converters import cry_table_to_schema

logger = logging.getLogger(__name__)


class CryService:
    def _get_user_pet(self, db: Session, pet_id: int, user_id: str) -> Optional[PetTable]:
        return db.query(PetTable).filter(
            PetTable.id == pet_id,
            PetTable.user_id == user_id
        ).first()

    def create_cry(self, db: Session, create_cry_input: CreateCryInput, user_id: str) -> Cry:
        try:
            pet = self._get_user_pet(db, create_cry_input.pet_id, user_id)
            if pet == None:
                raise UnauthorizedError(
                    "You are not authorized to view these cries")

            # Create CryTable instance with standardized state
            cry_table = CryTable.create(create_cry_input.model_dump())

            # Add and commit to the database
            db.add(cry_table)
            db.commit()
            db.refresh(cry_table)

            if cry_table is None:
                raise ValidationError("Failed to create cry")

            # Convert CryTable to Pydantic Cry model using utility function
            cry_pydantic = cry_table_to_schema(cry_table)
            return cry_pydantic

        except UnauthorizedError as pnfe:
            logger.error(pnfe)
            raise pnfe
        except (ValidationError) as custom_err:
            db.rollback()
            logger.error(f"Validation error: {custom_err}")
            raise custom_err
        except Exception as e:
            db.rollback()
            logger.exception("An error occurred while creating cry")
            raise ValidationError("Failed to create cry") from e

    def get_cry_by_id(self, db: Session, cry_id: int, user_id: str) -> Cry:
        try:
            cry_table = db.query(CryTable).join(PetTable).filter(
                CryTable.id == cry_id,
                PetTable.user_id == user_id
            ).first()
            if not cry_table:
                raise CryNotFoundError(f"Cry with id {cry_id} not found")

            cry_pydantic = cry_table_to_schema(cry_table)
            return cry_pydantic
        except CryNotFoundError as cnfe:
            logger.error(cnfe)
            raise cnfe
        except Exception as e:
            logger.exception("An error occurred while fetching cry by id")
            raise ValidationError("Failed to fetch cry") from e

    def get_all_cries_by_pet(self, db: Session, pet_id: int, user_id: str) -> list[Cry]:
        try:
            pet = self._get_user_pet(db, pet_id, user_id)
            if pet == None:
                raise UnauthorizedError(
                    "You are not authorized to view these cries")

            cry_tables = db.query(CryTable).filter(
                CryTable.pet_id == pet_id).all()

            return [cry_table_to_schema(cry) for cry in cry_tables]
        except UnauthorizedError as ue:
            logger.error(ue)
            raise ue
        except Exception as e:
            logger.exception(
                "An error occurred while fetching cries by pet id")
            raise ValidationError("Failed to fetch cries") from e

    def update_cry(self, db: Session, cry_id: int, update_cry_input: UpdateCryInput, user_id: str) -> Cry:
        try:
            cry_table = db.query(CryTable).join(PetTable).filter(
                CryTable.id == cry_id,
                PetTable.user_id == user_id
            ).first()
            if not cry_table:
                raise CryNotFoundError(f"Cry with id {cry_id} not found")

            # Update cry details
            cry_table.update(**update_cry_input.model_dump(exclude_unset=True))
            db.commit()
            db.refresh(cry_table)

            cry_pydantic = cry_table_to_schema(cry_table)
            return cry_pydantic
        except (ValidationError, CryNotFoundError) as custom_err:
            db.rollback()
            logger.error(f"Validation error: {custom_err}")
            raise custom_err
        except Exception as e:
            db.rollback()
            logger.exception("An error occurred while updating cry")
            raise ValidationError("Failed to update cry") from e

    def delete_cry(self, db: Session, cry_id: int, user_id: str) -> None:
        try:
            cry_table = db.query(CryTable).join(PetTable).filter(
                CryTable.id == cry_id,
                PetTable.user_id == user_id
            ).first()
            if not cry_table:
                raise CryNotFoundError(f"Cry with id {cry_id} not found")

            db.delete(cry_table)
            db.commit()
        except CryNotFoundError as cnfe:
            db.rollback()
            logger.error(cnfe)
            raise cnfe
        except Exception as e:
            db.rollback()
            logger.exception("An error occurred while deleting cry")
            raise ValidationError("Failed to delete cry") from e

    def get_pets_with_state(self, db: Session, pet_id: int, query_state: str, user_id: str) -> list[Cry]:
        try:
            standardized_state = CRY_STATE_KR_TO_EN.get(
                query_state, query_state)
            cry_tables = db.query(CryTable).join(PetTable).filter(
                CryTable.pet_id == pet_id,
                CryTable.state == standardized_state,
                PetTable.user_id == user_id
            ).all()
            cries_pydantic = [cry_table_to_schema(cry) for cry in cry_tables]
            return cries_pydantic
        except Exception as e:
            logger.exception(
                "An error occurred while fetching pets with specific state")
            raise ValidationError(
                "Failed to fetch pets with specified state") from e

    def get_pets_between_time(self, db: Session, pet_id: int, start_time: datetime, end_time: datetime, user_id: str) -> list[Cry]:
        try:
            cry_tables = db.query(CryTable).join(PetTable).filter(
                CryTable.pet_id == pet_id,
                CryTable.time >= start_time,
                CryTable.time <= end_time,
                PetTable.user_id == user_id
            ).all()
            cries_pydantic = [cry_table_to_schema(cry) for cry in cry_tables]
            return cries_pydantic
        except Exception as e:
            logger.exception(
                "An error occurred while fetching pets between times")
            raise ValidationError(
                "Failed to fetch pets between specified times") from e


cry_service = CryService()
