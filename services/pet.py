# services/pet.py
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import UploadFile
from PIL import Image
import os

from schemas.pet import *
from model.pet import PetTable
from enums.species import SpeciesEnum, SPECIES_KR_TO_EN
from error.exceptions import (
    NegativeAgeError, PetNotFoundError, WrongFileTypeError)
from utils.converters import pet_table_to_schema
from constants.path import PET_PROFILE_DIR


class PetService:
    def _get_pet_by_id(self, db: Session, pet_id: int, user_id: str) -> Optional[PetTable]:
        return db.query(PetTable).filter(PetTable.id == pet_id, PetTable.user_id == user_id).first()

    def create_pet(self, db: Session, create_pet_input: CreatePetInput, user_id: str) -> Pet:
        if create_pet_input.age < 0:
            raise NegativeAgeError("Age cannot be negative")

        pet_table = PetTable.create(
            user_id, create_pet_input.model_dump(exclude={'user_id'}))
        db.add(pet_table)
        db.commit()
        db.refresh(pet_table)

        return pet_table_to_schema(pet_table)

    def get_pet_by_id(self, db: Session, pet_id: int, user_id: str) -> Pet:
        pet_table = self._get_pet_by_id(db, pet_id, user_id)
        if not pet_table:
            raise PetNotFoundError(f"Pet with id {pet_id} not found")
        return pet_table_to_schema(pet_table)

    def get_all_pets_by_user(self, db: Session, user_id: str) -> list[Pet]:
        pet_tables = db.query(PetTable).filter(
            PetTable.user_id == user_id).all()
        return [pet_table_to_schema(pet) for pet in pet_tables]

    def update_pet(self, db: Session, pet_id: int, update_pet_input: UpdatePetInput, user_id: str) -> Pet:
        pet_table = self._get_pet_by_id(db, pet_id, user_id)
        if not pet_table:
            raise PetNotFoundError(f"Pet with id {pet_id} not found")

        if update_pet_input.age is not None and update_pet_input.age < 0:
            raise NegativeAgeError("Age cannot be negative")

        pet_table.update(**update_pet_input.model_dump(exclude_unset=True))
        db.commit()
        db.refresh(pet_table)

        return pet_table_to_schema(pet_table)

    def delete_pet(self, db: Session, pet_id: int, user_id: str) -> None:
        pet_table = self._get_pet_by_id(db, pet_id, user_id)
        if not pet_table:
            raise PetNotFoundError(f"Pet with id {pet_id} not found")

        db.delete(pet_table)
        db.commit()

    def uploadProfileImage(self, file: UploadFile, db: Session, pet_id: int, user_id: str):
        pet_table = self._get_pet_by_id(db, pet_id, user_id)
        if not pet_table:
            raise PetNotFoundError(f"Pet with id {pet_id} not found")

        # 파일 확장자를 file.filename에서 추출
        filename = file.filename
        if "." in filename:
            file_extension = filename.split(".")[-1].lower()
        else:
            raise WrongFileTypeError("파일 확장자를 찾을 수 없습니다.")

        # 이미지 파일 확장자만 허용 (jpg, jpeg, png, tiff, webp, heif, heic)
        allowed_extensions = ['jpg', 'jpeg',
                              'png', 'tiff', 'webp', 'heif', 'heic']
        if file_extension not in allowed_extensions:
            raise WrongFileTypeError("이미지만 받을 수 있습니다.")

        # 파일 저장 경로 설정 (항상 .jpeg로 저장)
        file_path = os.path.join(PET_PROFILE_DIR, f"{pet_id}.jpeg")

        # 파일을 jpeg로 변환 후 저장
        try:
            image = Image.open(file.file)
            rgb_image = image.convert("RGB")  # PNG, TIFF, HEIC 등은 RGB로 변환
            rgb_image.save(file_path, format="JPEG")
        except Exception as e:
            raise Exception(f"이미지 처리 중 오류가 발생했습니다: {str(e)}")

        return True


pet_service = PetService()
