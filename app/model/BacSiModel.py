from sqlalchemy import Column, ForeignKey, Integer

from app.model.NhanVienModel import NhanVien



class BacSi(NhanVien):
    __tablename__ = 'bacsi'

    # primary keys
    maBS = Column(Integer, ForeignKey(NhanVien.maNV), primary_key=True)
    # foreign key

    def __str__(self):
        return self.name
