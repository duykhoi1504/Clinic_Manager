from datetime import datetime
from sqlalchemy import  Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref

from app import db
from app.model.PersonModel import PersonModel
# from app.models import User


class NhanVien(PersonModel, db.Model):
    __tablename__ = 'nhanvien'

    # primary keys
    maNV = Column(Integer, primary_key=True, autoincrement=True)
    # attributes
    ngayVaoLam = Column(DateTime, default=datetime.now())
    # ChuyenNganh = Column(String(50))
    # avatar =Column(String(250), default='https://th.bing.com/th/id/OIP.48Pj-NVeziMTgdX6rHGpKAHaI1?w=162&h=194&c=7&r=0&o=5&dpr=1.1&pid=1.7')

    # user_id = Column(Integer, ForeignKey(User.id))
    def __str__(self):
        return self.name
