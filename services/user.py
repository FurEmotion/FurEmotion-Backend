from sqlalchemy.orm import Session
from typing import Optional

from schemas.user import *
from model.user import UserTable
from error.exceptions import (
    UserNotFoundError, UnauthorizedError,
    DuplicateEmailError, DuplicateUidError
)
from utils.converters import user_table_to_schema


class UserService:
    def _get_user_by_uid(self, db: Session, user_id: str) -> Optional[UserTable]:
        return db.query(UserTable).filter(UserTable.uid == user_id).first()

    def _get_user_by_email(self, db: Session, email: str) -> Optional[UserTable]:
        return db.query(UserTable).filter(UserTable.email == email).first()

    def _validate_unique_user(self, db: Session, create_user_input: CreateUserInput):
        if self._get_user_by_uid(db, create_user_input.uid):
            raise DuplicateUidError("User already exists")
        if self._get_user_by_email(db, create_user_input.email):
            raise DuplicateEmailError("Email already exists")

    def create_user(self, db: Session, create_user_input: CreateUserInput) -> User:
        self._validate_unique_user(db, create_user_input)

        user_table = UserTable(**create_user_input.model_dump())
        db.add(user_table)
        db.commit()
        db.refresh(user_table)

        return user_table_to_schema(user_table)

    def get_user_by_id(self, db: Session, user_id: str) -> User:
        user_table = self._get_user_by_uid(db, user_id)
        if not user_table:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return user_table_to_schema(user_table)

    def update_user(self, db: Session, user_id: str, update_user_input: UpdateUserInput) -> User:
        user_table = self._get_user_by_uid(db, user_id)
        if not user_table:
            raise UserNotFoundError(f"User with id {user_id} not found")
        user_table.update(**update_user_input.model_dump(exclude_unset=True))
        db.commit()
        db.refresh(user_table)

        return user_table_to_schema(user_table)

    def delete_user(self, db: Session, user_id: str) -> None:
        user_table = self._get_user_by_uid(db, user_id)
        if not user_table:
            raise UserNotFoundError(f"User with id {user_id} not found")
        db.delete(user_table)
        db.commit()

    def login(self, db: Session, login_user_input: LoginUserInput) -> User:
        user_table = self._get_user_by_email(db, login_user_input.email)
        if not user_table:
            raise UserNotFoundError(
                f"User with email {login_user_input.email} not found")
        if user_table.uid != login_user_input.uid:
            raise UnauthorizedError("Unauthorized user id")

        return user_table_to_schema(user_table)


user_service = UserService()
