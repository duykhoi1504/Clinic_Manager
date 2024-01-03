#Tác động tới CSDL
from sqlalchemy import Column, Integer, String,Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from app import db
from flask_login import UserMixin
import enum
from datetime import datetime

class UserRoleEnum(enum.Enum):
    USER=1
    ADMIN=2
    BACSI=3
    YTA=4
    THUNGAN=5

class Sex(enum.Enum):
    MALE = 0,
    FEMALE = 1


#UserMixin để nó hiều đây là model dùng để chứng thực-> vì Python da kế thừa
class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100), default='https://th.bing.com/th/id/OIP.48Pj-NVeziMTgdX6rHGpKAHaI1?w=162&h=194&c=7&r=0&o=5&dpr=1.1&pid=1.7')
    user_role = Column(Enum(UserRoleEnum),default=UserRoleEnum.USER)

    nhanvien = relationship('NhanVien', backref='user' , lazy=True)

    receipts = relationship('Receipt',backref='user',lazy=True)
    def __str__(self):
        return self.name

class BaseModel (db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)

class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False,unique=True)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return  self.name


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Float, default=0)
    image = Column(String(100))
    Category_ID = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)



class Receipt(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
# -----------------------------------------------------------------------


class PersonModel(object):
    # attributes
    hoTen = Column(String(50), default='')
    ngaySinh = Column(DateTime, default=datetime.now())
    maCCCD = Column(String(12), unique=True, default='')
    diaChi = Column(String(150), default='')
    email = Column(String(50), default='')
    soDienThoai = Column(String(10), default='')
    sex = Column(Enum(Sex), default=Sex.MALE)


class NhanVien(PersonModel, db.Model):
    __tablename__ = 'nhanvien'

    # primary keys
    maNV = Column(Integer, primary_key=True, autoincrement=True)
    # attributes
    ngayVaoLam = Column(DateTime, default=datetime.now())
    # ChuyenNganh = Column(String(50))
    avatar =Column(String(250), default='https://th.bing.com/th/id/OIP.48Pj-NVeziMTgdX6rHGpKAHaI1?w=162&h=194&c=7&r=0&o=5&dpr=1.1&pid=1.7')

    user_id = Column(Integer, ForeignKey(User.id))
    def __str__(self):
        return self.name


# class YTa(NhanVien):
#     __tablename__ = 'yta'
#     # primary key
#     maYT = Column(Integer, ForeignKey(NhanVien.maNV), primary_key=True)
#     # relationship
#
#     def __str__(self):
#         return self.name


class BacSi(NhanVien):
    __tablename__ = 'bacsi'

    # primary keys
    maBS = Column(Integer, ForeignKey(NhanVien.maNV), primary_key=True)
    # foreign key

    def __str__(self):
        return self.name


class BenhNhan(PersonModel, db.Model):
    __tablename__ = 'BenhNhan'

    # attribute
    maBN = Column(Integer, primary_key=True, autoincrement=True)
    tienSuBenh = Column(String(200), default='Không')
    lichkhambenh = relationship('LichKhamBenh', backref='benhnhan', lazy=True)

    def __str__(self):
        return self.name

class LichKhamBenh(db.Model):
    __tablename__ = 'lichkhambenh'

    # attribute
    id = Column(Integer, primary_key=True, autoincrement=True)
    loaiDangKi = Column(Integer, nullable=False)

    maBN = Column(Integer, ForeignKey(BenhNhan.maBN))
    def __str__(self):
        return self.name




if __name__=="__main__":
    from app import app
    with app.app_context():

        db.create_all()

        #########################
        import hashlib

        # u1 = User(name='BacSi',
        #           username='bacsi',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #           user_role=UserRoleEnum.BACSI)

        # u2 = User(name='Admin',
        #          username='admin',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.ADMIN
        #          )
        # u3 = User(name='VoDuyKhoi',
        #     username='voduykhoi',
        #     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #     user_role=UserRoleEnum.USER )
        # db.session.add_all([u1,u2,u3])
        # db.session.commit()
        #######################
        # d1 = BacSi(
        #     hoTen="Nguyễn Thị Thu Hồng",
        #     ngaySinh=datetime(1990, 1, 1),
        #     maCCCD="123456789012",
        #     diaChi="123 Main St",
        #     email="john.doe@example.com",
        #     soDienThoai="1234567890",
        #     sex=Sex.MALE,
        #     ngayVaoLam=datetime.now(),
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
        #     avatar="https://hoanmy.com/wp-content/uploads/2023/05/HMSGC-Bs-Thach-Minh-Huy.jpg"
        # )
        #
        #
        # db.session.add_all([d1, d2, d3, d4])
        # db.session.commit()
      #########################
        # c1 = Category(name="Iphone")
        # c2 = Category(name="tablet")
        #
        # db.session.add(c1)
        # db.session.add(c2)
        # db.session.commit()
        # ########################
        # p1 = Product(name="IPhone15 Pro Max", price=10000000, Category_ID=2, image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
        # p2 = Product(name="IPhone12 Pro Max", price=20000000, Category_ID=2, image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
        # p3 = Product(name="IPhone13 Pro Max", price=30000000, Category_ID=2,  image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
        # p4 = Product(name="IPhone16 Pro Max", price=40000000, Category_ID=1,  image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
        # p5 = Product(name="IPhone19 Pro Max", price=90000000, Category_ID=1,  image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
        # p6 = Product(name="Samsung", price=10000000, Category_ID=2, image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
        # p7 = Product(name="Oppo Pro Max", price=20000000, Category_ID=2, image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
        # p8 = Product(name="realme Pro Max", price=30000000, Category_ID=2,  image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
        # p9 = Product(name="Oppo 2", price=40000000, Category_ID=1,  image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
        # p10 = Product(name="Samsung2 Pro Max", price=90000000, Category_ID=1,  image= "https://mobilepriceall.com/wp-content/uploads/2022/09/Apple-iPhone-14-1024x1024.jpg")
        # db.session.add_all([p1, p2, p3, p4, p5,p6, p7, p8, p9, p10])
        # db.session.commit()
        # # #####
