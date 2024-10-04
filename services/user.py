# services/user.py
from sqlalchemy.orm import Session
import logging

from schemas.user import *
from model.user import UserTable
from error.exceptions import (
    ValidationError, UserNotFoundError,
    UnauthorizedError, DuplicateEmailError,
    DuplicateUidError
)
from utils.converters import user_table_to_schema

logger = logging.getLogger(__name__)


class UserService:
    def create_user(self, db: Session, create_user_input: CreateUserInput) -> User:
        try:
            # Check for duplicate uid
            existing_user = db.query(UserTable).filter(
                UserTable.uid == create_user_input.uid).first()
            if existing_user:
                raise DuplicateUidError("User already exists")

            # Check for duplicate email
            existing_user = db.query(UserTable).filter(
                UserTable.email == create_user_input.email).first()
            if existing_user:
                raise DuplicateEmailError("Email already exists")

            # Use UserTable.create to instantiate a new user
            print("Create Values: ", create_user_input.model_dump())
            user_table = UserTable.create(
                create_user_input.model_dump())

            # Add and commit to the database
            db.add(user_table)
            db.commit()
            db.refresh(user_table)

            if not user_table:
                raise ValidationError("Failed to create user")

            # Convert to Pydantic schema
            user_pydantic = user_table_to_schema(user_table)
            return user_pydantic

        except DuplicateUidError as due:
            db.rollback()
            logger.error(f"Duplicate uid error: {due}")
            raise due
        except DuplicateEmailError as dee:
            db.rollback()
            logger.error(f"Duplicate email error: {dee}")
            raise dee
        except Exception as e:
            db.rollback()
            logger.exception("An error occurred while creating user")
            raise ValidationError("Failed to create user") from e

    def get_user_by_id(self, db: Session, user_id: str) -> User:
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

    def login(self, db: Session, login_user_input: LoginUserInput) -> User:
        try:
            user_table = db.query(UserTable).filter(
                UserTable.email == login_user_input.email).first()
            if not user_table:
                raise UserNotFoundError(
                    f"User with email {login_user_input.email} not found")

            if user_table.uid != login_user_input.uid:
                raise UnauthorizedError("Unauthorized user id")

            user_pydantic = user_table_to_schema(user_table)
            return user_pydantic
        except UserNotFoundError as unfe:
            logger.error(f"User not found: {unfe}")
            raise unfe
        except UnauthorizedError as ue:
            logger.error(f"Unauthorized error: {ue}")
            raise ue
        except Exception as e:
            logger.exception("An error occurred while logging in user")
            raise ValidationError("Failed to login user") from e


user_service = UserService()
