from flask import Flask, render_template, Blueprint, request

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=["POST", "GET"])
def signup():
    return render_template('signup.html')

@auth.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')
@auth.route('/home', methods=['POST','GET'])
def home():
    return render_template('home.html')
@auth.route('/sell',methods=['POST','GET'])
def sell():
    return render_template('sell.html')