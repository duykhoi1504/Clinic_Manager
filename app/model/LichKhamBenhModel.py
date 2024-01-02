from sqlalchemy import Column, Integer, ForeignKey
from app import db
from app.model import BenhNhanModel



class LichKhamBenh(db.Model):
    __tablename__ = 'lichkhambenh'

    # attribute
    id = Column(Integer, primary_key=True, autoincrement=True)
    thuTuKham=Column(Integer, nullable=False)
    loaiDangKi = Column(Integer, nullable=False)


    maBN= Column(Integer, ForeignKey(BenhNhanModel.BenhNhan.maBN))


    def __str__(self):
        return self.name

