from flask import Flask, request, render_template, Blueprint
from .views import views
from .auth import auth
import os


def create_app():
    #Making the static and template folders
    base_dir = os.path.abspath(os.path.dirname(__file__))
    static_dir = os.path.join(base_dir, '..', 'static')
    template_dir = os.path.join(base_dir, '..', 'templates')
    app = Flask(__name__,static_folder=static_dir, template_folder=template_dir)

    #registering the blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    return app

