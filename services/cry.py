# services/cry.py
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from typing import Optional
import os
import json
import pandas as pd
from sqlalchemy.dialects import sqlite
from fastapi import UploadFile

from schemas.cry import *
from model.cry import CryTable
from model.pet import PetTable
from error.exceptions import (
    CryNotFoundError, UnauthorizedError, WrongCryOfSpeciesError)
from utils.converters import cry_table_to_schema
from enums.cry_state import check_right_cry_state
from constants.path import CRY_INSPECT_LOG_DIR, CRY_DATASET_DIR
from services.cry_predict import cry_predict


class CryService:
    def _get_user_pet(self, db: Session, pet_id: int, user_id: str) -> Optional[PetTable]:
        return db.query(PetTable).filter(
            PetTable.id == pet_id,
            PetTable.user_id == user_id
        ).first()

    async def create_cry(self, db: Session, create_cry_input: CreateCryInput, user_id: str) -> Cry:
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
            CryTable.time <= end_time + timedelta(days=1),
            PetTable.user_id == user_id
        ).all()
        return [cry_table_to_schema(cry) for cry in cry_tables]

    def inspect_cry(self, db: Session, pet_id: int, user_id: str):
        # 유저의 반려동물인지 확인
        pet = self._get_user_pet(db, pet_id, user_id)
        if not pet:
            raise UnauthorizedError(
                "You are not authorized to view cries for this pet")

        # 분석 기간 설정
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        # 파일 이름 설정: 로그 파일이 있는 경우 가져오며 그렇지 않을 경우 분석을 수행
        file_name = f"{pet.id}_{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}"
        file_path = os.path.join(CRY_INSPECT_LOG_DIR, f'{file_name}.json')

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                res = json.loads(f.read())
            return res

        query = db.query(CryTable).filter(
            CryTable.pet_id == pet_id,
            CryTable.time >= start_date,
            CryTable.time <= end_date
        )
        sql_query = query.statement.compile(
            dialect=sqlite.dialect(), compile_kwargs={"literal_binds": True})

        df = pd.read_sql(sql_query, db.connection())

        if len(df) < 100:
            return None

        try:
            # 1. 주로 우는 시간대 분석
            cry_freq_hour = df['time'].dt.hour.value_counts().sort_index()

            # 2. 일별 울음 빈도 분석
            cry_freq_date = df[['id']].groupby(
                df['time'].dt.date).count().reset_index()
            cry_freq_date['time'] = cry_freq_date['time'].astype(str)

            # 3. 울음 원인 빈도 분석
            type_freq = df['state'].value_counts()
            type_freq.sort_values(ascending=True, inplace=True)

            # 4. 울음 원인에 따른 울음 지속시간 분석
            duration_of_type = df[['state', 'duration']
                                  ].groupby('state').mean()
            duration_of_type.sort_values(by='duration', inplace=True)

            min_value = duration_of_type['duration'].min().astype(int)
            duration_of_type['duration'] -= min_value
            bar_percent = (duration_of_type['duration'] /
                           duration_of_type['duration'].max()).round(3)

            inspect_result = {
                'logId': file_name,
                'cry_freq_hour': cry_freq_hour.tolist(),
                'cry_freq_date': {
                    'date': cry_freq_date['time'].tolist(),
                    'freqs': cry_freq_date['id'].tolist()
                },
                'type_freq': type_freq.to_dict(),
                'duration_of_type': {
                    'type': duration_of_type.index.tolist(),
                    'duration': duration_of_type['duration'].round(3).tolist(),
                    'bar_percent': bar_percent.tolist()
                }
            }

            # 결과를 파일로 저장
            with open(file_path, 'w') as f:
                f.write(json.dumps(inspect_result, indent=4, ensure_ascii=False))

            return inspect_result

        except Exception as e:
            raise Exception(f"Failed to inspect cry: {e}")

    async def predict_cry(self, db: Session, file: UploadFile, pet_id: int, user_id: str) -> Cry:
        # 유저의 반려동물인지 확인
        pet = self._get_user_pet(db, pet_id, user_id)
        if not pet:
            raise UnauthorizedError(
                "You are not authorized to view cries for this pet")

        # 반려동물 울음 분석
        content = await file.read()
        predictMap = await cry_predict(content, pet.species, user_id)

        # wav 파일 저장
        curtime = datetime.now()
        timestamp = curtime.strftime("%Y%m%d-%H%M%S")
        file_id = f'{pet_id}_{timestamp}'
        file_path = os.path.join(CRY_DATASET_DIR, f"{file_id}.wav")
        with open(file_path, 'wb') as f:
            f.write(content)

        # 분석 결과 DB에 저장
        create_cry_input = CreateCryInput(
            pet_id=pet_id,
            time=curtime,
            state=max(predictMap, key=predictMap.get),
            audioId=file_id,
            predictMap=predictMap,
        )
        print("create cry: ", create_cry_input)
        cry = await self.create_cry(db, create_cry_input, user_id)

        return cry


cry_service = CryService()
