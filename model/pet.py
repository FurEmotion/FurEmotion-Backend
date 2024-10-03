# model/pet.py
from __future__ import annotations
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db import DB_Base
from enums.species import KR_TO_EN


class PetTable(DB_Base):
    __tablename__ = 'pet'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    species = Column(String, nullable=False)
    photo_id = Column(String, nullable=True)
    sub_species = Column(String, nullable=False)

    # Foreign key to UserTable
    user_id = Column(String, ForeignKey('user.uid'), nullable=False)

    # Relationship to UserTable
    owner = relationship("UserTable", back_populates="pets")

    # Relationship to CryTable
    cries = relationship("CryTable", back_populates="pet",
                         cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        species = kwargs.get('species')
        if species in KR_TO_EN:
            kwargs['species'] = KR_TO_EN[species]
        super().__init__(**kwargs)

    def __repr__(self):
        return (f"<Pet(id={self.id}, name={self.name}, gender={self.gender}, "
                f"photo_id={self.photo_id}, age={self.age}, species={self.species}, "
                f"sub_species={self.sub_species})>")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "age": self.age,
            "photo_id": self.photo_id,
            "species": self.species,
            "sub_species": self.sub_species
        }

    def update(self, **kwargs):
        if 'species' in kwargs:
            species = kwargs['species']
            if species in KR_TO_EN:
                kwargs['species'] = KR_TO_EN[species]
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    def update_from_dict(self, data: dict):
        species = data.get('species')
        if species in KR_TO_EN:
            data['species'] = KR_TO_EN[species]
        return self.update(**data)