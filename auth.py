from flask import Flask, render_template, Blueprint, request, redirect, session, url_for
from model import User
from pymongo import MongoClient
from dotenv import load_dotenv
from utils import generate_otp, send_otp
import os
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
print(f"Loaded MONGO_URI: {MONGO_URI}")
client = MongoClient(MONGO_URI)
db = client['Student-Community']
users_collection = db['users']

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method=='POST':
        data = {
            "full_name": request.form.get('full_name'),
            "enrollment": request.form.get('enrollment'),
            "email": request.form.get('email'),
            "contact": request.form.get('contact'),
            "college": request.form.get('college'),
            "course": request.form.get('course'),
            "branch": request.form.get('branch'),
            "section": request.form.get('section'),
            "password": request.form.get('password'),
        }

        # Validations
        email = data['email']
        enrollment = data['enrollment']
        contact = data['contact']
        
        if not email.endswith(('@gmail.com', '@outlook.com')):
            return render_template('signup.html', error='Only Gmail or Outlook emails are allowed.')

        if not (enrollment.isdigit() and len(enrollment) == 10):
            return render_template('signup.html', error='Enrollment number must be exactly 10 digits.')

        if not (contact.isdigit() and len(contact) == 10):
            return render_template('signup.html', error='Contact number must be exactly 10 digits.')
        
        new_user = User(data)
        success, message = new_user.save_to_db()
        if(success):
            otp = generate_otp()
            new_user.update_otp(otp)
            send_otp(data['email'], otp)
            session['user'] = {
                'full_name': data['full_name'],
                'email': data['email'],
                'contact': data['contact']
            }
            return redirect(url_for('auth.verifyotp'))
        else:
            return redirect(url_for('auth.signup'))

    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if User.check_password(email, password):
            user = User.get_data(email)
            session['user'] = {
                'full_name': user['full_name'],
                'email': user['email'],
                'contact': user['contact']
            }
            return redirect(url_for('views.test'))
        else:
            print("e")
    return render_template('login.html')

@auth.route('/verifyotp', methods=['POST','GET'])
def verifyotp():
    if request.method=='POST':
        n_user = session.get('user')
        email = n_user.get('email')
        user = User.get_data(email)
        user_otp = user.get("otp")
        entered_otp = "".join([
            request.form.get('otp1', ''),
            request.form.get('otp2', ''),
            request.form.get('otp3', ''),
            request.form.get('otp4', ''),
            request.form.get('otp5', ''),
            request.form.get('otp6', '')
        ])
        if(user_otp==entered_otp):
            users_collection.update_one({"email": email}, {"$set": {"isVerified": True}})
            session['user'] = {
                    'full_name': user['full_name'],
                    'email': user['email'],
                    'contact': user['contact']
                }
            return redirect(url_for('views.test'))
        else:
            return "invalid otp entered."
    return render_template('verifyOTP.html')

@auth.route('/resendOTP')
def resendOTP():
    n_user = session.get('user')