# services/user.py
from sqlalchemy.orm import Session
import logging

from schemas.user import *
from model.user import UserTable
from error.exceptions import (
    ValidationError, UserNotFoundError,
    UnauthorizedError, DuplicateEmailError
)
from utils.converters import user_table_to_schema

logger = logging.getLogger(__name__)


class UserService:
    def create_user(self, db: Session, create_user_input: CreateUserInput) -> User:
        try:
            # Check for duplicate email
            existing_user = db.query(UserTable).filter(
                UserTable.email == create_user_input.email).first()
            if existing_user:
                raise DuplicateEmailError("Email already exists")

            # Use UserTable.create to instantiate a new user
            user_table = UserTable.create(
                email=create_user_input.email,
                nickname=create_user_input.nickname,
                photoId=create_user_input.photoId
            )

            # Add and commit to the database
            db.add(user_table)
            db.commit()
            db.refresh(user_table)

            if not user_table:
                raise ValidationError("Failed to create user")

            # Convert to Pydantic schema
            user_pydantic = user_table_to_schema(user_table)
            return user_pydantic

        except DuplicateEmailError as dee:
            db.rollback()
            logger.error(f"Duplicate email error: {dee}")
            raise dee
        except Exception as e:
            db.rollback()
            logger.exception("An error occurred while creating user")
            raise ValidationError("Failed to create user") from e

    def get_current_user(self, db: Session, user_id: str) -> User:
        try:
            user_table = db.query(UserTable).filter(
                UserTable.uid == user_id).first()
            if not user_table:
                raise UserNotFoundError(f"User with id {user_id} not found")
            user_pydantic = user_table_to_schema(user_table)
            return user_pydantic
        except UserNotFoundError as unfe:
            logger.error(f"User not found: {unfe}")
            raise unfe
        except Exception as e:
            logger.exception("An error occurred while fetching current user")
            raise ValidationError("Failed to fetch user") from e

    def get_user_by_id(self, db: Session, target_user_id: str) -> User:
        try:
            user_table = db.query(UserTable).filter(
                UserTable.uid == target_user_id).first()
            if not user_table:
                raise UserNotFoundError(
                    f"User with id {target_user_id} not found")
            user_pydantic = user_table_to_schema(user_table)
            return user_pydantic
        except UserNotFoundError as unfe:
            logger.error(f"User not found: {unfe}")
            raise unfe
        except Exception as e:
            logger.exception("An error occurred while fetching user by id")
            raise ValidationError("Failed to fetch user") from e

    def update_user(self, db: Session, user_id: str, update_user_input: UpdateUserInput) -> User:
        try:
            user_table = db.query(UserTable).filter(
                UserTable.uid == user_id).first()
            if not user_table:
                raise UserNotFoundError(f"User with id {user_id} not found")

            # Update user details using the update method
            update_data = update_user_input.model_dump(exclude_unset=True)
            if 'email' in update_data:
                # Check for duplicate email
                existing_user = db.query(UserTable).filter(
                    UserTable.email == update_data['email']).first()
                if existing_user and existing_user.uid != user_id:
                    raise DuplicateEmailError("Email already exists")

            user_table.update(**update_data)
            db.commit()
            db.refresh(user_table)

            user_pydantic = user_table_to_schema(user_table)
            return user_pydantic

        except (DuplicateEmailError, UserNotFoundError) as custom_err:
            db.rollback()
            logger.error(f"Validation error: {custom_err}")
            raise custom_err
        except Exception as e:
            db.rollback()
            logger.exception("An error occurred while updating user")
            raise ValidationError("Failed to update user") from e

    def delete_user(self, db: Session, user_id: str) -> None:
        try:
            user_table = db.query(UserTable).filter(
                UserTable.uid == user_id).first()
            if not user_table:
                raise UserNotFoundError(f"User with id {user_id} not found")

            db.delete(user_table)
            db.commit()
        except UserNotFoundError as unfe:
            db.rollback()
            logger.error(f"User not found: {unfe}")
            raise unfe
        except Exception as e:
            db.rollback()
            logger.exception("An error occurred while deleting user")
            raise ValidationError("Failed to delete user") from e
