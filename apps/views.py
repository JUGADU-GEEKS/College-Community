from flask import Flask, Blueprint, render_template, request

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('welcome.html')