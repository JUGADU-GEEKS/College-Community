from flask import Flask, render_template, Blueprint, request

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=["POST", "GET"])
def signup():
    return render_template('signup.html')

@auth.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')