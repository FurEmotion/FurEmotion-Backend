# services/pet.py
from sqlalchemy.orm import Session
import logging

from schemas.pet import CreatePetInput, Pet
from model.pet import PetTable
from enums.species import SpeciesEnum, KR_TO_EN
from error.exceptions import NegativeAgeError, InvalidSpeciesError, ValidationError
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
