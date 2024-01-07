import datetime
import json

from flask_login import current_user
from sqlalchemy.sql.elements import and_
from app.models import  BenhNhan,Thuoc,BacSi

from app import db
def get_customer_id_card_eq(maCCCD=None):
    return db.session.query(BenhNhan.maCCCD) \
        .filter(BenhNhan.maCCCD.__eq__(maCCCD)) \
        .all()


def get_medicine_name(tenThuoc=None):
    return db.session.query(Thuoc.name) \
        .filter(Thuoc.name.__eq__(tenThuoc)) \
        .all()


# def get_medicine_unit(medicine_name=None):
#     return db.session.query(MedicineUnitModel.name) \
#         .join(MedicineModel) \
#         .filter(and_(MedicineUnitModel.medicine_unit_id.__eq__(MedicineModel.medicine_unit_id),
#                      MedicineModel.name.__eq__(str(medicine_name).strip()))) \
#         .first()


