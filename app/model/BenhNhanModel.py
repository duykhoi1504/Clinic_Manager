from sqlalchemy import Column, Integer
from sqlalchemy.orm import backref, relationship

from app import db
from app.model.PersonModel import PersonModel


class BenhNhan(PersonModel, db.Model):
    __tablename__ = 'BenhNhan'

    # attribute
    customer_id = Column(Integer, primary_key=True, autoincrement=True)


    def __str__(self):
        return self.name

