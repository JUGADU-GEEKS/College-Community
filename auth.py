from flask import Flask, render_template, Blueprint, request, redirect, session, url_for
from model import User
from pymongo import MongoClient
from dotenv import load_dotenv
from utils import generate_otp, send_otp
import os
import re
load_dotenv()
import bcrypt

MONGO_URI = os.getenv("MONGO_URI")
print(f"Loaded MONGO_URI: {MONGO_URI}")
client = MongoClient(MONGO_URI)
db = client['Student-Community']
users_collection = db['users']

auth = Blueprint('auth', __name__)

def is_valid_password(password):
    pattern = r'^(?=.*[A-Z])(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$'
    return re.match(pattern, password)

def is_valid_linkedin_url(url):
    pattern = r'^https?://(www\.)?linkedin\.com/(in|pub|company)/[a-zA-Z0-9_-]+/?$'
    return re.match(pattern, url) is not None

@auth.before_app_request

def require_login():
    from flask import request
    # Only require login for /home and its subroutes
    if request.path.startswith('/home'):
        if 'user' not in session:
            return redirect(url_for('auth.login'))

@auth.route('/')
def index():
    return render_template('welcome.html')

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
            "linkedin": request.form.get('linkedin'),
        }

        # Validations
        email = data['email']
        enrollment = data['enrollment']
        contact = data['contact']
        password = data['password']
        confirm_password = request.form.get('confirm-password')
        linkedin = data['linkedin']
        u = users_collection.find_one({"email":email})
        
        if u:
            return redirect('/login')
        if not is_valid_linkedin_url(linkedin):
            return render_template('signup.html', error='Linkedin URL is not correct.')
        if not email.endswith(('@gmail.com', '@outlook.com')):
            return render_template('signup.html', error='Only Gmail or Outlook emails are allowed.')
        if not (contact.isdigit() and len(contact) == 10):
            return render_template('signup.html', error='Contact number must be exactly 10 digits.')
        
        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match.')
        #to check for password constraints
        if not is_valid_password(password):
            return render_template('signup.html', error='Password Should be atleast 8 character long, should have one uppercase and one special character.')
        
        

        
        new_user = User(data)
        success, message = new_user.save_to_db()
        if(success):
            print(data)
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
            user_NonVerified = users_collection.find_one({"email":email, "isVerified": False})
            if(user_NonVerified):
                return redirect(url_for("auth.resendotp"))
            return redirect(url_for('views.home'))
        else:
            return render_template('login.html', error='Invalid email or password.')

    return render_template('login.html')

@auth.route('/verifyotp', methods=['POST','GET'])
def verifyotp():
    message = request.args.get('message') or None  # Get message from query parameters

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
            return redirect(url_for('views.home'))
        else:
            return "invalid otp entered."
    return render_template('verifyOTP.html', message=message)

@auth.route('/resendotp', methods=['GET'])
def resendotp():
    # Get the user from session
    session_user = session.get('user')
    email = session_user.get('email')

    # Fetch the actual User object from the database
    user = User.get_data(email)
    if not user:
        return "User not found.", 404

    # Generate and update OTP
    otp = generate_otp()
    users_collection.update_one(
        {"email": email},
        {"$set": {"otp": otp, "isVerified": False}}
    )
    send_otp(email, otp)

    # Redirect to OTP verification page
    return redirect(url_for('auth.verifyotp', message = "OTP Sent Again !"))



@auth.route('/forget_Password', methods=['POST'])
def forget_password():
    email = request.form.get('email')
    user = users_collection.find_one({"email": email})

    if not user:
        return render_template('login.html', error="Email not registered")

    # Generate and send OTP
    otp = generate_otp()
    users_collection.update_one({"email": email}, {"$set": {"otp": otp}})
    send_otp(email, otp)

    # Store email in session for verification
    session['reset_email'] = email
    return redirect(url_for('auth.verify_reset_otp'))

@auth.route('/verify_reset_otp', methods=['GET', 'POST'])
def verify_reset_otp():
    if request.method == 'POST':
        email = session.get('reset_email')
        if not email:
            return redirect(url_for('auth.forget_password'))

        user = users_collection.find_one({"email": email})
        entered_otp = "".join([
            request.form.get('otp1', ''),
            request.form.get('otp2', ''),
            request.form.get('otp3', ''),
            request.form.get('otp4', ''),
            request.form.get('otp5', ''),
            request.form.get('otp6', '')
        ])

        if user and user.get("otp") == entered_otp:
            return redirect(url_for('auth.reset_password'))
        else:
            return render_template('verify_reset_otp.html', error="Invalid OTP. Please try again.")

    return render_template('verify_reset_otp.html')


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = session.get('reset_email')
        if not email:
            return redirect(url_for('auth.forget_password'))

        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Password validation (same as signup)
        if new_password != confirm_password:
            return render_template('reset_password.html', error="Passwords do not match.")
        
        if len(new_password) < 8:
            return render_template('reset_password.html', error="Password must be at least 8 characters long.")
        
        if not re.search(r'[A-Z]', new_password):
            return render_template('reset_password.html', error="Password must contain at least one uppercase letter.")
        
        if not re.search(r'[a-z]', new_password):
            return render_template('reset_password.html', error="Password must contain at least one lowercase letter.")
        
        if not re.search(r'\d', new_password):
            return render_template('reset_password.html', error="Password must contain at least one digit.")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
            return render_template('reset_password.html', error="Password must contain at least one special character (!@#$%^&* etc.).")

        # Update password in database
        User.update_password(email, new_password)        
        
        # Clear session and redirect to login
        session.pop('reset_email', None)
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html')




@auth.route('/adminLogin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Determine which admin is logging in
        if email == os.getenv("ADMIN_EMAIL_BPIT"):
            stored_password = os.getenv("ADMIN_PASSWORD_BPIT")
            college_name = "Bhagwan Parshuram Institute of Technology"
        elif email == os.getenv("ADMIN_EMAIL_DTU"):
            stored_password = os.getenv("ADMIN_PASSWORD_DTU")
            college_name = "Delhi Technological University"
        else:
            return render_template('error.html', message='Invalid Credentials')

        if not bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return render_template('error.html', message='Invalid Credentials')

        # Store user and college info in session
        session['user'] = {'email': email, 'college': college_name}

        return redirect(url_for('views.admin_dashboard'))

    return render_template('adminlogin.html')


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))