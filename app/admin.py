from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from app import app, db, dao
from app.models import Category, Product, NhanVien, BenhNhan, DanhSachKhamBenh,Thuoc,User

from flask_login import logout_user, current_user
from flask import redirect,url_for
from app.models import UserRoleEnum


# hàm đổ thông tin ra ngoài dể làm báo cáo thống kê
class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=dao.count_products_by_cate())


admin = Admin(app=app, name="Quan ly ban hang", template_mode="bootstrap4", index_view=MyAdminIndex())


# XAC THUC TAI KHOAN
# kiem tra co phai tai khoan user
class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


# class AuthenticatedNhanVien(BaseView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.user_role not in [UserRoleEnum.ADMIN]
#

# kiem tra co phai tai khoan BacSi
class AuthenticatedBacSi(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role in [UserRoleEnum.BACSI, UserRoleEnum.ADMIN]


# kiem tra co phai tai khoan Y tá
class AuthenticatedYTa(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role in [UserRoleEnum.YTA, UserRoleEnum.ADMIN]


class AuthenticatedBacSiAndYTa(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role in [UserRoleEnum.YTA, UserRoleEnum.BACSI]


# kiem tra co phai tai khoan Thu Ngan
class AuthenticatedYThuNgan(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role in [UserRoleEnum.THUNGAN, UserRoleEnum.ADMIN]


# kiem tra co phai tai khoan Admin
class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


#############################################


class MyProductView(AuthenticatedAdmin):
    column_display_pk = True
    column_list = ['id', 'name', 'price', 'category']
    column_searchable_list = ['name']
    column_filters = ['name', 'price']
    can_export = True
    can_view_details = True


class MyCategoryVIew(AuthenticatedAdmin):
    column_list = ['name', 'products']


class MyStatsView(BaseView):
    @expose('/')
    def index(self):
        if not self.is_accessible():
            return redirect(url_for('admin.index'))
        return self.render('admin/stats.html',role=current_user.user_role,
                                                        UserRoleEnum=UserRoleEnum,
                                                        stats=dao.count_products_by_cate())
    def is_accessible(self):
        # Kiểm tra nếu người dùng là admin
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN

class MyTacVuNhanVienView(AuthenticatedUser, BaseView):
    @expose('/')
    def index(self):
        if not self.is_accessible():
            return self.render('admin/login')
        return self.render('admin/thongtinnhanvien.html', role=current_user.user_role, UserRoleEnum=UserRoleEnum)




class MyLogoutView(AuthenticatedUser):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class MyNhanVienView(AuthenticatedAdmin):
    column_display_pk = True
    column_list = ['maNV', 'hoTen', 'maCCCD','user','user_id']
    column_searchable_list = ['hoTen']
    column_filters = ['maNV', 'hoTen', 'maCCCD']
    can_export = True
    can_view_details = True

class MyUserView(AuthenticatedAdmin):
    column_display_pk = True
    column_list = ['name', 'username', 'password', 'user_role']
    column_searchable_list = ['name']
    column_filters = ['name', 'username', 'password', 'user_role']
    can_export = True
    can_view_details = True

    # # Add a file upload field for the 'avatar' attribute
    # form_extra_fields = {
    #     'avatar': FileUploadField('Avatar', base_path='path/to/upload/folder')
    # }


class MyBenhNhanView(AuthenticatedBacSiAndYTa):
    # column_list = True
    column_display_pk = True
    column_searchable_list = ['hoTen']
    column_filters = ['maBN', 'hoTen', 'diaChi', 'soDienThoai']
    can_export = True
    can_view_details = True


#DÀNH CHO ADMIN
class MyDanhSachKhamBenhView(AuthenticatedAdmin):
    # column_list = ['id', 'soLuongBenhNhanToiDa']
    column_display_pk = True
    column_searchable_list = ['id']
    column_filters = ['id']
    can_export = True
    can_view_details = True
  # Add a file upload field for the 'avatar' attribute
  #   form_extra_fields = {
  #       'avatar': FileUploadField('Avatar', base_path='path/to/upload/folder')
  #   }

class MyThuocView(AuthenticatedAdmin):

    column_searchable_list = ['tenThuoc','nhaSX']
    column_filters = ['tenThuoc','nhaSX','giaTien']
    column_hide_backrefs = False
    can_create = True
    can_edit = True
    can_delete = True
    create_modal = True
    edit_modal = True
    details_modal = True
    column_display_pk = True
    page_size = 10
    column_display_all_relations = True
    can_view_details = True
    can_export = True


admin.add_view(MyDanhSachKhamBenhView(DanhSachKhamBenh, db.session,name='Danh Sách Khám Bệnh'))
admin.add_view(MyBenhNhanView(BenhNhan, db.session, name='bệnh nhân'))
admin.add_view(MyThuocView(Thuoc, db.session, name='Thuốc'))
admin.add_view(MyNhanVienView(NhanVien, db.session,name='Nhân viên'))
admin.add_view(MyUserView(User, db.session))
admin.add_view(MyCategoryVIew(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(MyStatsView(name='Thống kê báo cáo'))

admin.add_view(MyTacVuNhanVienView(name='Thông tin'))
admin.add_view(MyLogoutView(name='Đăng xuất'))
