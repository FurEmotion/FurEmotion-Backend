# model/user.py
from __future__ import annotations
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db_base import DB_Base


class UserTable(DB_Base):
    __tablename__ = 'user'
    uid = Column(String, primary_key=True, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    nickname = Column(String, nullable=False)
    photoId = Column(String, nullable=True)

    # Relationship to PetTable
    pets = relationship("PetTable", back_populates="owner",
                        cascade="all, delete-orphan", lazy='noload')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def create(cls, data: dict) -> UserTable:
        return cls(**data)

    def __repr__(self):
        return f"<User(uid={self.uid}, email={self.email}, nickname={self.nickname}, photoId={self.photoId})>"

    def to_dict(self):
        return {
            "uid": self.uid,
            "email": self.email,
            "nickname": self.nickname,
            "photoId": self.photoId
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self
