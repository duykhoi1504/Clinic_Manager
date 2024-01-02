from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from app import app, db, dao
from app.models import Category, Product,NhanVien

from flask_login import logout_user, current_user
from flask import redirect
from app.models import UserRoleEnum
from flask_admin.form import FileUploadField
from wtforms import StringField



#hàm đổ thông tin ra ngoài dể làm báo cáo thống kê
class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=dao.count_products_by_cate())


admin = Admin(app=app, name="Quan ly ban hang", template_mode="bootstrap4", index_view=MyAdminIndex())


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class MyProductView(AuthenticatedAdmin):
    column_display_pk = True
    column_list = ['id', 'name', 'price', 'category']
    column_searchable_list = ['name']
    column_filters =['name', 'price']
    can_export = True
    can_view_details = True



class MyCategoryVIew(AuthenticatedAdmin):
    column_list = ['name', 'products']


class MyStatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class MyLogoutView(AuthenticatedUser):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')




class NhanVienView(AuthenticatedAdmin):
    column_list = ['maNV', 'hoTen', 'ngayVaoLam', 'diaChi', 'email']
    column_display_pk = True
    column_searchable_list = ['hoTen']
    column_filters = ['maNV', 'hoTen', 'ngayVaoLam', 'diaChi', 'email']
    can_export = True
    can_view_details = True

    # Add a file upload field for the 'avatar' attribute
    form_extra_fields = {
        'avatar': FileUploadField('Avatar')
    }


admin.add_view(NhanVienView(NhanVien, db.session))
admin.add_view(MyCategoryVIew(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(MyStatsView(name='Thong ke bao cao'))
admin.add_view(MyLogoutView(name='Đăng xuất'))
