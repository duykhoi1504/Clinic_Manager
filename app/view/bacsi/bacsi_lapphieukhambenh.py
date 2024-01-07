import math

from flask import render_template, request, redirect, session, jsonify, flash, url_for
from app import dao, utils
from app import app, login, db
from flask_login import login_user, logout_user
from app.models import NhanVien, UserRoleEnum, BenhNhan
from datetime import datetime
from app.admin import current_user



# @app.route('/api/lapphieukham/<hoTen>', methods=['PUT'])
# def find_benhnhan(hoTen):
#     benhnhans = session.get('cart', {})
#     if benhnhans and hoTen in benhnhans:
#         existing_benhnhan = BenhNhan.query.filter_by(hoTen=hoTen).first()
#
#     session['cart'] = benhnhans
#
#     return jsonify({
#         'benhnhan': BenhNhan.query.filter_by(hoTen=hoTen).first()
#     })


# @app.route('/api/fetch_patient_info', methods=['POST'])
# def fetch_patient_info():
#     # Get the patient's name from the AJAX request
#     patient_name = request.form.get('patientName')
#
#     # Query the database for patient information
#     patient = BenhNhan.query.filter_by(name=patient_name).first()
#
#     # Check if the patient exists
#     if patient:
#         # Prepare the JSON response
#         patient_info = {
#             'name': patient.name,
#             'maCCCD': patient.maCCCD,
#             'tienSuBenh': patient.tienSuBenh,
#             # Add more fields as needed
#         }
#         return jsonify(patient_info)
#     else:
#         # Patient not found, return an empty response or an error message
#         return jsonify({'error': 'Patient not found'})