import math

from flask import render_template, request, redirect, session, jsonify,flash
import dao, utils
from app import app, login
from flask_login import login_user, logout_user
from app.models import NhanVien,UserRoleEnum
from datetime import datetime
from app.admin import current_user

@app.route("/")
def index():
    kw = request.args.get('kw')
    page = request.args.get('page')
    cates = dao.load_categories()
    products=dao.load_products(kw=kw,page=page)
    nhanviens=dao.load_nhanviens(kw=kw,page=page)


    image_data = [
        {'url': 'https://hoanmy.com/wp-content/uploads/2023/12/dai-thao-duong.png', 'title': 'Những biến chứng nguy hiểm của đái tháo đường và cách phòng ngừa',
         'content': 'Thời gian gần đây, tỷ lệ người bệnh đái tháo đường đang gia tăng khá cao. Theo số liệu từ Hiệp hội Đái tháo đường Thế giới (International Diabetes Federation – IDF), vào năm 2019, thế giới có khoảng 463 triệu người mắc bệnh đái tháo đường. Trong số đó, ước tính hơn 4 triệu […]'},
        {'url': 'https://hoanmy.com/wp-content/uploads/2023/12/suy-gian-tinh-mach-1706-x-1080-px.png', 'title': 'Cách phòng ngừa, điều trị suy giãn tĩnh mạch để tránh biến chứng về sau',
         'content': 'Suy giãn tĩnh mạch là căn bệnh phổ biến hiện nay, ảnh hưởng tới chất lượng cuộc sống người bệnh. Nếu không được điều trị đúng cách, bệnh có thể gây nên nhiều biến chứng nguy hiểm. Hãy cùng bệnh viện Hoàn Mỹ Sài Gòn tìm hiểu về cách phòng ngừa và điều trị suy […]'},
        # Thêm các phần tử khác nếu cần
        {'url': 'https://hoanmy.com/wp-content/uploads/2023/11/AdobeStock_455652091-scaled.jpeg', 'title': 'Điều trị ung thư dạ dày ở đâu tốt?',
         'content': 'Theo số liệu từ Globocan 2020, ung thư dạ dày thuộc nhóm có tỷ lệ tử vong cao thứ 3 tại Việt Nam, và ngày nay loại ung thư này đang có xu hướng trẻ hóa. Chính vì thế, việc nắm được các dấu hiệu của bệnh ung thư dạ dày và tầm soát sức […]'},
        {'url': 'https://hoanmy.com/wp-content/uploads/2023/10/BCSCHU1-1.jpg', 'title': 'Hạ đường huyết có nguy hiểm không? Nguyên nhân và cách xử trí',
         'content': 'Hạ đường huyết là tình trạng dễ gặp ở người bệnh đái tháo đường hoặc người ăn uống không khoa học. Đây là dấu hiệu cảnh báo một số vấn đề nghiêm trọng của cơ thể, cần phát hiện kịp thời và có biện pháp xử lý nhanh để tránh biến chứng nguy hiểm. Hạ […]'},
    ]
    total = dao.count_product()

    return render_template("index.html",
                           products=products,nhanviens=nhanviens,
                           image_data=image_data,
                           pages=math.ceil(total / app.config['PAGE_SIZE']),
                           role=current_user.user_role if current_user.is_authenticated else None,)


@app.route("/datlichkham",methods=['post', 'get'])
def add_benh_nhan():
    err_msg = ""
    success_message = ""
    if request.method.__eq__('POST'):
        hoTen = request.form.get('hoTen')
        ngaySinh = request.form.get('ngaySinh')
        maCCCD = request.form.get('maCCCD')
        diaChi = request.form.get('diaChi')
        email = request.form.get('email')
        soDienThoai = request.form.get('soDienThoai')
        tienSuBenh = request.form.get('tienSuBenh')
        sex = request.form.get('sex')

        if not all([hoTen, ngaySinh, maCCCD, diaChi, email, soDienThoai, tienSuBenh, sex]):
            err_msg = "Please fill in all required fields."
            return render_template("BenhNhan.html", err_msg=err_msg)
        try:
            dao.add_benhnhan(hoTen=hoTen,ngaySinh=ngaySinh,maCCCD=maCCCD,diaChi=diaChi,email=email,soDienThoai=soDienThoai,tienSuBenh=tienSuBenh,sex=sex)
            success_message = "BenhNhan added successfully!"
            err_msg = ""
        except:
            success_message = ""
            err_msg = "he thong dang loi!"

        return render_template("BenhNhan.html", err_msg=err_msg,success_message=success_message)
    return render_template("BenhNhan.html", err_msg=err_msg,success_message=success_message)

@app.route('/thanhtoan',methods=['post', 'get'])
def thanhtoan():
    return render_template("thungan.html")

@app.route('/dangkikhamtructiep',methods=['post', 'get'])
def dangkionline():
    err_msg = ""
    success_message = ""
    if request.method.__eq__('POST'):
        hoTen = request.form.get('hoTen')
        ngaySinh = request.form.get('ngaySinh')
        maCCCD = request.form.get('maCCCD')
        diaChi = request.form.get('diaChi')
        email = request.form.get('email')
        soDienThoai = request.form.get('soDienThoai')
        tienSuBenh = request.form.get('tienSuBenh')
        sex = request.form.get('sex')

        if not all([hoTen, ngaySinh, maCCCD, diaChi, email, soDienThoai, tienSuBenh, sex]):
            err_msg = "Please fill in all required fields."
            return render_template("yta.html", err_msg=err_msg)
        try:
            dao.add_benhnhan(hoTen=hoTen, ngaySinh=ngaySinh, maCCCD=maCCCD, diaChi=diaChi, email=email,
                             soDienThoai=soDienThoai, tienSuBenh=tienSuBenh, sex=sex)
            success_message = "BenhNhan added successfully!"
            err_msg = ""
        except:
            success_message = ""
            err_msg = "he thong dang loi!"

        return render_template("yta.html", err_msg=err_msg, success_message=success_message)
    return render_template("yta.html", err_msg=err_msg, success_message=success_message)

@app.route('/lapphieukham',methods=['post', 'get'])
def lapphieukham():
    return render_template("bacsi.html")

@app.route('/aboutus')
def aboutus():
    return render_template("about_us.html")


@app.route('/doingu')
def doingu():
    return render_template("client_doingu.html")



@app.route("/nhanvien/<id>")
def details(id):
    nhanvien = NhanVien.query.get(id)
    return render_template('details.html', nhanvien=nhanvien,datetime=datetime)


@app.route('/login',methods=['post', 'get'])
def login_user_process():
    isCorrect = True;
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
        else:
            isCorrect = False;
            return render_template('login.html',isCorrect=isCorrect)
        next = request.args.get('next')
        return  redirect('/' if next is None else next)
    return render_template('login.html',isCorrect=isCorrect)


@app.route('/logout')
def logout_user_process():
    logout_user()
    return redirect("/login")


@app.route('/register', methods=['post', 'get'])
def register_user():
    err_msg = ""
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            try:
                dao.add_user(name=request.form.get('name'),
                             username=request.form.get('username'),
                             password=password,
                             avatar=request.files.get('avatar'))
            except:
                err_msg='he thong dang bi loi!!!'
            else:
                return redirect('/login')
            #avatar là lấy từ trường name trong register.html
            # request.files['avatar']
        else:
            err_msg="Mật khẩu ko khớp!!!!!"

    return render_template('register.html', err_msg=err_msg)


@app.route("/admin/login", methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/api/cart', methods=['post'])
def add_cart():
    cart = session.get('cart')
    if cart is None:
        cart = {}
    data = request.json
    id = str(data.get("id"))

    if id in cart:  # san pham da co trong gio
        cart[id]["quantity"] = cart[id]["quantity"]+1
    else:  # san pham chua co trong gio
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1
        }
    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/<product_id>', methods=['put'])
def update_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        quantity = request.json.get('quantity')
        cart[product_id]['quantity'] = int(quantity)

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        del cart[product_id]

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/pay', methods=['post'])
def pay():
    try:
        dao.add_receipt(session.get('cart'))
    except:
        return jsonify({'status': 500, 'err_msg': 'he thong dang co loi'})
    else:
        del session['cart']
        return jsonify({'status': 200})


@app.route('/cart')
def cart_list():
    return render_template('cart.html')



@app.route("/testhtml")
def index1():
    return render_template("testhtml.html")


@app.context_processor#trang nao cung se co du lieu nay`
def common_resp():
    role = current_user.user_role if current_user.is_authenticated else None
    return{
        'caregories': dao.load_categories(),
        'cart': utils.count_cart(session.get('cart')),
        'UserRoleEnum':UserRoleEnum,
        'role':role
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    from app import admin
    app.run(debug=True)