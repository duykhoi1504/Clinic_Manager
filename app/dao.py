# truy xuất Csdl
from app.models import Category, Product, User, Receipt, ReceiptDetails, NhanVien, BenhNhan,BacSi,Thuoc
import hashlib
from app import app, db
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func
from flask import session


def load_categories():
    return Category.query.all()
def load_thuocs():
    return Thuoc.query.all()


def load_products(kw=None, page=None):
    products = Product.query
    if kw:
        products = products.filter(Product.name.contains((kw)))

    if page:
        page = int(page)
        page_size = app.config["PAGE_SIZE"]
        start = (page - 1) * page_size
        return products.slice(start, start + page_size)

    return products.all()


def load_benhnhans(kw=None):
    benhnhans = BenhNhan.query
    if kw:
        benhnhans = benhnhans.filter(BenhNhan.maBN.contains((kw)))

    return benhnhans.all()

def load_bacsis(kw=None):
    bacsi = BacSi.query
    if kw:
        bacsi = bacsi.filter(BacSi.maBN.contains((kw)))

    return bacsi.all()
def load_nhanviens(kw=None, page=None,user_role=None):
    nhanviens = NhanVien.query
    if kw:
        nhanviens = nhanviens.filter(NhanVien.hoTen.contains((kw)))

    if user_role:
        nhanviens = nhanviens.join(User).filter(User.user_role == user_role)

    if page:
        page = int(page)
        page_size = app.config["PAGE_SIZE"]
        start = (page - 1) * page_size
        return nhanviens.slice(start, start + page_size)

    return nhanviens.all()


def count_product():
    return Product.query.count()


def get_user_by_id(id):
    return User.query.get(id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password)

    if avatar:
        res = cloudinary.uploader.upload((avatar))
        print(res)
        u.avatar = res['secure_url']

    db.session.add(u)
    db.session.commit()


def add_benhnhan(hoTen, ngaySinh, maCCCD, diaChi, email, soDienThoai, tienSuBenh, sex):
    BN = BenhNhan(hoTen=hoTen, ngaySinh=ngaySinh, maCCCD=maCCCD, diaChi=diaChi, email=email,
                  soDienThoai=soDienThoai, tienSuBenh=tienSuBenh, sex=sex)
    db.session.add(BN)
    db.session.commit()


def add_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'],
                               price=c['price'],
                               receipt=r,
                               product_id=c['id'])
            db.session.add(d)
        db.session.commit()





#########################
def save_benhnhan_data_to_session(hoTen, ngaySinh, maCCCD, diaChi, email, soDienThoai, tienSuBenh, sex):
    if 'benhnhan_data' not in session:
        session['benhnhan_data'] = {}
    benhnhan_data = session['benhnhan_data']

    # Kiểm tra xem maCCCD đã tồn tại trong cả database và session hay chưa
    existing_benhnhan = BenhNhan.query.filter_by(maCCCD=maCCCD).first()
    maCCCD_in_session = maCCCD in benhnhan_data

    if existing_benhnhan or maCCCD_in_session:
        return False  # Báo hiệu trùng mã CCCD
    benhnhan_data[maCCCD] = {
        'hoTen': hoTen,
        'ngaySinh': ngaySinh,
        'maCCCD': maCCCD,
        'diaChi': diaChi,
        'email': email,
        'soDienThoai': soDienThoai,
        'tienSuBenh': tienSuBenh,
        'sex': sex
    }
    return True

#--------------------KIỂM TRA NHẬP DỮ LIỆU BỆNH NHÂN---------------------
# Hàm để xác nhận và nhập vào cơ sở dữ liệu
def confirm_benhnhan_and_insert_to_database():
    benhnhan_data = session.get('benhnhan_data', {})

    if benhnhan_data:
        # Thực hiện các kiểm tra hoặc xác nhận cần thiết
        # Ví dụ: bạn có thể in dữ liệu ra console để kiểm tra
        print("Dữ liệu Bệnh nhân trong session:", benhnhan_data)

        # Sau khi xác nhận, bạn có thể thực hiện nhập vào cơ sở dữ liệu
        # Thực hiện nhập vào cơ sở dữ liệu ở đây
        for data in benhnhan_data.values():
            # Thực hiện nhập vào cơ sở dữ liệu, ví dụ:
            BN = BenhNhan(hoTen=data['hoTen'],
                          ngaySinh=data['ngaySinh'],
                          maCCCD=data['maCCCD'],
                          diaChi=data['diaChi'],
                          email=data['email'],
                          soDienThoai=data['soDienThoai'],
                          tienSuBenh=data['tienSuBenh'],
                          sex=data['sex'])
            db.session.add(BN)
            db.session.commit()

    # Sau khi nhập, xóa dữ liệu từ session
    session.pop('benhnhan_data')




def count_products_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
            .join(Product, Product.Category_ID == Category.id, isouter=True).group_by(Category.id).all()

#-----------------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        print(count_products_by_cate())
