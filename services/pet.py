# services/pet.py
from sqlalchemy.orm import Session
import logging

from schemas.pet import *
from model.pet import PetTable
from enums.species import SpeciesEnum, SPECIES_KR_TO_EN
from error.exceptions import NegativeAgeError, InvalidSpeciesError, ValidationError, PetNotFoundError, UnauthorizedError
from utils.converters import pet_table_to_schema

logger = logging.getLogger(__name__)


class PetService:
    def create_pet(self, db: Session, create_pet_input: CreatePetInput, user_id: str) -> Pet:
        try:
            # Validate age
            if create_pet_input.age < 0:
                raise NegativeAgeError("Age cannot be negative")

            # Create PetTable instance with standardized species
            pet_table = PetTable.create(
                user_id, create_pet_input.model_dump(exclude={'user_id'}))

            # Add and commit to the database
            db.add(pet_table)
            db.commit()
            db.refresh(pet_table)

            if pet_table is None:
                raise ValidationError("Failed to create pet")

            # Convert PetTable to Pydantic Pet model using utility function
            pet_pydantic = pet_table_to_schema(pet_table)
            return pet_pydantic

        except (NegativeAgeError, InvalidSpeciesError) as custom_err:
            db.rollback()
            logger.error(f"Validation error: {custom_err}")
            raise custom_err
        except Exception as e:
            db.rollback()
            logger.exception("An error occurred while creating pet")
            raise ValidationError("Failed to create pet") from e

    def get_pet_by_id(self, db: Session, pet_id: int, user_id: str) -> Pet:
        try:
            pet_table = db.query(PetTable).filter(
                PetTable.id == pet_id, PetTable.user_id == user_id).first()
            if not pet_table:
                raise PetNotFoundError(f"Pet with id {pet_id} not found")
            pet_pydantic = pet_table_to_schema(pet_table)
            return pet_pydantic
        except PetNotFoundError as pnfe:
            logger.error(pnfe)
            raise pnfe
        except Exception as e:
            logger.exception("An error occurred while fetching pet by id")
            raise ValidationError("Failed to fetch pet") from e

    def get_all_pets_by_user(self, db: Session, user_id: str) -> list[Pet]:
        try:
            pet_tables = db.query(PetTable).filter(
                PetTable.user_id == user_id).all()
            pets_pydantic = [pet_table_to_schema(pet) for pet in pet_tables]
            return pets_pydantic
        except Exception as e:
            logger.exception("An error occurred while fetching user's pets")
            raise ValidationError("Failed to fetch pets") from e

    def update_pet(self, db: Session, pet_id: int, update_pet_input: UpdatePetInput, user_id: str) -> Pet:
        try:
            pet_table = db.query(PetTable).filter(
                PetTable.id == pet_id, PetTable.user_id == user_id).first()
            if not pet_table:
                raise PetNotFoundError(f"Pet with id {pet_id} not found")

            # Validate age if it's being updated
            if update_pet_input.age is not None and update_pet_input.age < 0:
                raise NegativeAgeError("Age cannot be negative")

            # Update pet details
            pet_table.update(**update_pet_input.model_dump(exclude_unset=True))
            db.commit()
            db.refresh(pet_table)

            pet_pydantic = pet_table_to_schema(pet_table)
            return pet_pydantic
        except (NegativeAgeError, InvalidSpeciesError, PetNotFoundError) as custom_err:
            db.rollback()
            logger.error(f"Validation error: {custom_err}")
            raise custom_err
        except Exception as e:
            db.rollback()
            logger.exception("An error occurred while updating pet")
            raise ValidationError("Failed to update pet") from e

    def delete_pet(self, db: Session, pet_id: int, user_id: str) -> None:
        try:
            pet_table = db.query(PetTable).filter(
                PetTable.id == pet_id, PetTable.user_id == user_id).first()
            if not pet_table:
                raise PetNotFoundError(f"Pet with id {pet_id} not found")

            db.delete(pet_table)
            db.commit()
        except PetNotFoundError as pnfe:
            db.rollback()
            logger.error(pnfe)
            raise pnfe
        except Exception as e:
            db.rollback()
            logger.exception("An error occurred while deleting pet")
            raise ValidationError("Failed to delete pet") from e


pet_service = PetService()
