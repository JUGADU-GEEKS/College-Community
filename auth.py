from flask import Flask, render_template, Blueprint, request, redirect, session, url_for
from model import User

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
        otp = request.form.get('otp')
        new_user = User(data)
        success, message = new_user.save_to_db()
        if(success):
            session['user'] = {
                'full_name': data['full_name'],
                'email': data['email'],
                'contact': data['contact']
            }
            return redirect(url_for('views.test'))
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

