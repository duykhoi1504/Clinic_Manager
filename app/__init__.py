#Khởi tạo
from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
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

##############INIT VALUES DATABASE###########

# from models import QuyDinh
#
# def initValuesForTable():
#     try:
#         #ADD QUY DINH
#         quydinh1 = QuyDinh(tenQD='Quy định 1', noiDung='Nội dung quy định 1')
#         quydinh2 = QuyDinh(tenQD='Quy định 2', noiDung='Nội dung quy định 2')
#         db.session.add_all([quydinh1,quydinh2])
#     except:
#         db.session.rollback()
#



