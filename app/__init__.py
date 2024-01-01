#Khởi tạo
from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.model.PersonModel import Sex
from datetime import datetime
app=Flask(__name__)

app.secret_key="Admin@123456789"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@localhost/clinicdb' % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"]=6


db = SQLAlchemy(app)
login = LoginManager(app=app)

import cloudinary

cloudinary.config(
    cloud_name="dx5nqi4ll",
    api_key="362937263322676",
    api_secret="w339Gv4z_NcM7gvOPmiq5QloAB0"
)



from app.model.PersonModel import PersonModel
from app.model.BacSiModel import BacSi
from app.model.BenhNhanModel import BenhNhan
from app.model.NhanVienModel import NhanVien
from app.model.YTaModel import YTa

def initTables():
    try:
        db.create_all()
    except:
        db.session.rollback()




def createValues():
    # d1 = BacSi(
    #     hoTen="Nguyễn Thị Thu Hồng",
    #     ngaySinh=datetime(1990, 1, 1),
    #     maCCCD="123456789012",
    #     diaChi="123 Main St",
    #     email="john.doe@example.com",
    #     soDienThoai="1234567890",
    #     sex=Sex.MALE,
    #     ngayVaoLam=datetime.now(),
    #     ChuyenNganh="Nam Khoa",
    #     avatar="https://hoanmy.com/wp-content/uploads/2023/05/HMSGC-Bs-Phan-Thanh-Tuoi.jpg"
    #
    # )
    # d2 = BacSi(
    #     hoTen="Phan Thanh Tươi",
    #     ngaySinh=datetime(2003, 1, 1),
    #     maCCCD="123456789013",
    #     diaChi="127 Main St",
    #     email="ThanhDat@example.com",
    #     soDienThoai="1234567891",
    #     sex=Sex.MALE,
    #     ngayVaoLam=datetime(2020, 2, 1),
    #     ChuyenNganh="Specialization",
    #     avatar="https://hoanmy.com/wp-content/uploads/2023/05/HMSGC-Bs-Phan-Thanh-Tuoi.jpg"
    #
    # )
    # d3 = BacSi(
    #     hoTen="Đặng Thị Thu Bé",
    #     ngaySinh=datetime(2003, 1, 1),
    #     maCCCD="123456789014",
    #     diaChi="127 Main St",
    #     email="ThanhDat@example.com",
    #     soDienThoai="1234567891",
    #     sex=Sex.MALE,
    #     ngayVaoLam=datetime(2020, 2, 1),
    #     ChuyenNganh="Specialization",
    #     avatar="https://hoanmy.com/wp-content/uploads/2023/05/HMSGC-THAY-THUOC-UU-TU.-DANG-THI-BE-THU.jpg"
    #
    # )
    # d4 = BacSi(
    #     hoTen="Thạch Minh Huy",
    #     ngaySinh=datetime(2003, 1, 1),
    #     maCCCD="123456789015",
    #     diaChi="127 Main St",
    #     email="ThanhDat@example.com",
    #     soDienThoai="1234567891",
    #     sex=Sex.MALE,
    #     ngayVaoLam=datetime(2020, 2, 1),
    #     ChuyenNganh="Specialization",
    #     avatar="https://hoanmy.com/wp-content/uploads/2023/05/HMSGC-Bs-Thach-Minh-Huy.jpg"
    # )



    db.session.add_all([d1, d2, d3, d4])
    db.session.commit()