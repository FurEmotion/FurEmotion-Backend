from __future__ import annotations
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, JSON, Float
from sqlalchemy.orm import relationship, declarative_base
from pydantic import BaseModel
import uuid
from db import DB_Base
from schemas.cry import Cry


class CryTable(DB_Base):
    __tablename__ = 'cry'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pet_id = Column(Integer, ForeignKey('pet.id'), nullable=False)
    time = Column(DateTime, nullable=False)
    state = Column(String, nullable=False)
    audioId = Column(String, nullable=False)
    predictMap = Column(JSON, nullable=False)
    intensity = Column(String(1), default='u')
    duration = Column(Float, default=2.0)

    # Relationship to PetTable
    pet = relationship("PetTable", back_populates="cries")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Cry(id={self.id}, pet_id={self.pet_id}, time={self.time}, state={self.state}, audioId={self.audioId}, predictMap={self.predictMap}, intensity={self.intensity}, duration={self.duration})>"

    def to_dict(self):
        return {
            "id": self.id,
            "pet_id": self.pet_id,
            "time": self.time,
            "state": self.state,
            "audioId": self.audioId,
            "predictMap": self.predictMap,
            "intensity": self.intensity,
            "duration": self.duration
        }

    def to_model(self):
        return Cry(**self.to_dict())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    def update_from_model(self, model: Cry):
        return self.update(**model.dict())

    def update_from_dict(self, data: dict):
        return self.update(**data)
