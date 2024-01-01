from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import backref, relationship

from app.model.NhanVienModel import NhanVien



class YTa(NhanVien):
    __tablename__ = 'yta'
    # primary key
    maYT = Column(Integer, ForeignKey(NhanVien.maNV), primary_key=True)
    # relationship

    def __str__(self):
        return self.name