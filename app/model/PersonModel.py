import enum
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Enum


class Sex(enum.Enum):
    MALE = 0,
    FEMALE = 1


class PersonModel(object):
    # attributes
    hoTen = Column(String(50), default='')
    ngaySinh = Column(DateTime, default=datetime.now())
    maCCCD = Column(String(12), unique=True, default='')
    diaChi = Column(String(150), default='')
    email = Column(String(50), default='')
    soDienThoai = Column(String(10), default='')
    sex = Column(Enum(Sex), default=Sex.MALE)

