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
    def __str__(self):
        return self.name


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




class YTa(NhanVien):
    __tablename__ = 'yta'
    # primary key
    maYT = Column(Integer, ForeignKey(NhanVien.maNV), primary_key=True)
    # relationship
    danhsachkhamBenh_id = relationship('DanhSachKhamBenh', backref='thungan', lazy=True)
    def __str__(self):
        return self.name


class BacSi(NhanVien):
    __tablename__ = 'bacsi'

    # primary keys
    maBS = Column(Integer, ForeignKey(NhanVien.maNV), primary_key=True)
    # foreign key

    #relationships
    phieuKhamBenh = relationship('PhieuKhamBenh', backref='bacsi', lazy=True)
    def __str__(self):
        return self.name



class ThuNgan(NhanVien):
    __tablename__ = 'thungan'
    # primary key
    thuNgan_id = Column(Integer, ForeignKey(NhanVien.maNV), primary_key=True)
    hoadonthanhtoan = relationship('HoaDonThanhToan', backref='thungan', lazy=True)

    def __str__(self):
        return self.name


class BenhNhan(PersonModel, db.Model):
    __tablename__ = 'BenhNhan'

    # attribute
    maBN = Column(Integer, primary_key=True, autoincrement=True)
    tienSuBenh = Column(String(200), default='Không')
    lichkhambenh_id = relationship('LichKhamBenh', backref='benhnhan', lazy=True)

    def __str__(self):
        return self.name


class DanhSachKhamBenh(db.Model):
    __tablename__ = 'danhsachkhambenh'
    id = Column(Integer, primary_key=True, autoincrement=True)
    soLuongBenhNhanToiDa = Column(Integer, default=40)
    YTa_ID= Column(Integer, ForeignKey(YTa.maYT))

    lichkhambenh_id = relationship('LichKhamBenh', backref='danhsachkhambenh', lazy=True)
    bieumau = relationship('BieuMau', backref='danhsachkhambenh', lazy=True)
    quanly = relationship('QuanLy', backref='danhsachkhambenh', lazy=True)

    def __str__(self):
        return self.name



class LichKhamBenh(db.Model):
    __tablename__ = 'lichkhambenh'

    # attribute
    id = Column(Integer, primary_key=True, autoincrement=True)


    maBN = Column(Integer, ForeignKey(BenhNhan.maBN))
    dsKhamBenh_id=Column(Integer, ForeignKey(DanhSachKhamBenh.id))

    bieumau = relationship('BieuMau', backref='lichkhambenh', lazy=True)
    def __str__(self):
        return self.name

class QuyDinh(db.Model):
    __tablename__ = 'quydinh'
    maQD = Column(Integer, primary_key=True, autoincrement=True)
    tenQD = Column(String(50), nullable=False)
    noiDung = Column(String(200), nullable=False)

    quanly = relationship('QuanLy', backref='quydinh', lazy=True)

    def __str__(self):
        return self.name

class DonVi(db.Model):
    __tablename__ = 'donvi'
    maDV = Column(Integer, primary_key=True, autoincrement=True)
    tenDV = Column(String(50), nullable=False)

    thuoc = relationship('Thuoc', backref='donvi', lazy=True)
    def __str__(self):
        return self.name

class Thuoc(db.Model):
    __tablename__ = 'thuoc'
    maThuoc = Column(Integer, primary_key=True, autoincrement=True)
    tenThuoc = Column(String(50), nullable=False)
    moTa = Column(String(250), nullable=True)
    ngaySX=Column(DateTime, default=datetime.now(),nullable=False)
    nhaSX= Column(String(250), nullable=False)
    soLuong=Column(Integer,nullable=False)
    giaTien = Column(Float, default=0)
    image = Column(String(250),default='https://data-service.pharmacity.io/pmc-upload-media/production/pmc-ecm-core/__sized__/products/P00222_11-thumbnail-510x510-70.jpg')

    # foreign key
    maDV_id=Column(Integer, ForeignKey(DonVi.maDV))

    #relationships
    danhsachthuoc = relationship('DanhSachThuoc', backref='thuoc', lazy=True)
    huongdansudung = relationship('HuongDanSuDung', backref='thuoc', lazy=True)
    quanly = relationship('QuanLy', backref='thuoc', lazy=True)

    def __str__(self):
        return self.name


class PhieuKhamBenh(db.Model):
    __tablename__ = 'phieukhambenh'
    maPhieuKham= Column(Integer, primary_key=True, autoincrement=True)
    trieuChung=Column(String(250), nullable=False)
    duDoanBenh=Column(String(100), nullable=False)

    bacsi_ID=Column(Integer, ForeignKey(BacSi.maBS))
    huongdansudung = relationship('HuongDanSuDung', backref='phieukhambenh', lazy=True)
    hoadonthanhtoan = relationship('HoaDonThanhToan', backref='phieukhambenh', lazy=True)
    bieumau = relationship('BieuMau', backref='phieukhambenh', lazy=True)
    quanly = relationship('QuanLy', backref='phieukhambenh', lazy=True)

    def __str__(self):
        return self.name


class HuongDanSuDung(db.Model):
    __tablename__ = 'huongdansudung'
    maThuoc_id=Column(Integer, ForeignKey(Thuoc.maThuoc),primary_key=True)
    maPhieuKham_id=Column(Integer, ForeignKey(PhieuKhamBenh.maPhieuKham),primary_key=True)
    lieuDung = Column(String(100), nullable=False)
    cachDung = Column(String(250), nullable=False)
    def __str__(self):
        return self.name

class DanhSachThuoc(db.Model):
    __tablename__ = 'danhsachthuoc'
    maDS = Column(Integer, primary_key=True, autoincrement=True)
    maThuoc_id=Column(Integer, ForeignKey(Thuoc.maThuoc))

    quanly = relationship('QuanLy', backref='danhsachthuoc', lazy=True)

    def __str__(self):
        return self.name

class HoaDonThanhToan(db.Model):
    __tablename__ = 'hoadonthanhtoan'
    maHD = Column(Integer, primary_key=True, autoincrement=True)
    tienKham=Column(Float,nullable=False)
    tienThuoc=Column(Float,nullable=False)
    tongTien=Column(Float,nullable=False)
    thuNgan_id=Column(Integer, ForeignKey(ThuNgan.thuNgan_id))
    maPhieuKham=Column(Integer, ForeignKey(PhieuKhamBenh.maPhieuKham))

    bieumau = relationship('BieuMau', backref='hoadonthanhtoan', lazy=True)
    quanly = relationship('QuanLy', backref='hoadonthanhtoan', lazy=True)

    def __str__(self):
        return self.name



class BieuMau(db.Model):
    __tablename__ = 'bieumau'
    maBM= Column(Integer, primary_key=True, autoincrement=True)
    tenBM=Column(String(250), nullable=False)
    ngayKham = Column(DateTime, default=datetime.now())


    maPhieuKham=Column(Integer, ForeignKey(PhieuKhamBenh.maPhieuKham))
    hoaDon_id = Column(Integer, ForeignKey(HoaDonThanhToan.maHD))
    dsKhamBenh_id = Column(Integer, ForeignKey(DanhSachKhamBenh.id))
    lichKhamBenh = Column(Integer, ForeignKey(LichKhamBenh.id))


    def __str__(self):
        return self.name

#QuanLy

class QuanLy(db.Model):
    __tablename__ = 'quanly'
    quanLy_id= Column(Integer, primary_key=True, autoincrement=True)
    dsThuoc_id=Column(Integer, ForeignKey(DanhSachThuoc.maDS))
    thuoc_id = Column(Integer, ForeignKey(Thuoc.maThuoc))
    quyDinh_id = Column(Integer, ForeignKey(QuyDinh.maQD))
    maPhieuKham_id = Column(Integer, ForeignKey(PhieuKhamBenh.maPhieuKham))
    hoaDon_id = Column(Integer, ForeignKey(HoaDonThanhToan.maHD))
    danhSachKhamBenh_id = Column(Integer, ForeignKey(DanhSachKhamBenh.id))

    admin = relationship('Admin', backref='quanly', lazy=True)

    def __str__(self):
        return self.name


class Admin(NhanVien):
    __tablename__ = 'admin'
    # primary key
    admin_id = Column(Integer, ForeignKey(NhanVien.maNV), primary_key=True)
    quanLy_id = Column(Integer, ForeignKey(QuanLy.quanLy_id),primary_key=True)

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
        # u4 = User(name='thungan',
        #     username='thungan',
        #     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #     user_role=UserRoleEnum.YTA )
        # u5 = User(name='thungan',
        #           username='thungan',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #           user_role=UserRoleEnum.THUNGAN)
        # db.session.add_all([u1,u2,u3,u4,u5])

        #db.session.commit()
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
        ## #########################
        #values thungan
        # yta1 = YTa(
        #     hoTen="Nguyễn Văn Y ",
        #     ngaySinh=datetime(2003, 1, 1),
        #     maCCCD="123456789016",
        #     diaChi="123 Đường Chính",
        #     email="yta1@example.com",
        #     soDienThoai="1234567890",
        #     sex=Sex.MALE,
        #     ngayVaoLam=datetime(2017, 4, 20),
        #     avatar="https://res.cloudinary.com/dx9eo8pyh/image/upload/v1704361418/yta_qwimqb.png",
        #
        # )
        #
        # yta2 = YTa(
        #     hoTen="Trần Thị Mỹ",
        #     ngaySinh=datetime(2003, 2, 1),
        #     maCCCD="987654321017",
        #     diaChi="456 Đường Sồi",
        #     email="yta2@example.com",
        #     soDienThoai="0987654321",
        #     sex=Sex.FEMALE,
        #     ngayVaoLam=datetime(2018, 5, 25),
        #     avatar="https://res.cloudinary.com/dx9eo8pyh/image/upload/v1704361418/yta_qwimqb.png",
        #
        # )
        #
        # yta3 = YTa(
        #     hoTen="Lê Văn Sĩ",
        #     ngaySinh=datetime(2003, 3, 1),
        #     maCCCD="111222333444",
        #     diaChi="789 Đường Thông",
        #     email="yta3@example.com",
        #     soDienThoai="5556667777",
        #     sex=Sex.MALE,
        #     ngayVaoLam=datetime(2019, 8, 13),
        #     avatar="https://res.cloudinary.com/dx9eo8pyh/image/upload/v1704361418/yta_qwimqb.png",
        #
        # )
        #
        # yta4 = YTa(
        #     hoTen="Phạm Thị Nơ",
        #     ngaySinh=datetime(2003, 4, 1),
        #     maCCCD="555666777888",
        #     diaChi="987 Đường Phố",
        #     email="yta4@example.com",
        #     soDienThoai="4443332222",
        #     sex=Sex.FEMALE,
        #     ngayVaoLam=datetime(2015, 6, 10),
        #     avatar="https://res.cloudinary.com/dx9eo8pyh/image/upload/v1704361418/yta_qwimqb.png",
        #
        # )
        #
        # yta5 = YTa(
        #     hoTen="Võ Văn Kiệt",
        #     ngaySinh=datetime(2003, 7, 1),
        #     maCCCD="999888777666",
        #     diaChi="654 Đường Cây",
        #     email="yta5@example.com",
        #     soDienThoai="1112223333",
        #     sex=Sex.MALE,
        #     ngayVaoLam=datetime(2015, 3, 15),
        #     avatar="https://res.cloudinary.com/dx9eo8pyh/image/upload/v1704361418/yta_qwimqb.png",
        #
        # )
        # db.session.add_all([yta1,yta2,yta3,yta4,yta5])
        # db.session.commit()
        #Values Yta
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
