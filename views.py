from flask import Flask, Blueprint, render_template, request, session
from model import User

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('welcome.html')

@views.route('/test')
def test():
    user_new = session.get('user')
    email = user_new.get('email')
    user = User.get_data(email)
    return render_template('test.html', user=user)

@views.route('/home', methods=['POST','GET'])
def home():
    return render_template('home.html')

@views.route('/sell',methods=['POST','GET'])
def sell():
    return render_template('sell.html')