from sqlalchemy import Column, Integer
from sqlalchemy.orm import backref, relationship

from app import db
from app.model.PersonModel import PersonModel


class BenhNhan(PersonModel, db.Model):
    __tablename__ = 'BenhNhan'

    # attribute
    maBN = Column(Integer, primary_key=True, autoincrement=True)

    lichkhambenh = relationship('lichkhambenh', backref=backref('benhnhan', lazy=True))

    def __str__(self):
        return self.name

