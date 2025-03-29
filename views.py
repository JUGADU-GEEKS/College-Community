from flask import Flask, Blueprint, render_template, request, session, jsonify
from model import User
from price_predict import predict_price_equipment, predict_price_calculator
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

@views.route('/price',methods=['POST','GET'])
def price():
    predicted_price = None
    if request.method == 'POST':
        item_type = request.form.get('itemType')
        print("Form submitted with item type:", item_type)  # Debug print
        
        if item_type == 'equipment':
            equipment_item = request.form.get('equipmentItem')
            months_old = request.form.get('monthsOld')
            condition = request.form.get('condition')
            predicted_price = predict_price_equipment(equipment_item, int(months_old), condition)
            
        elif item_type == 'calculator':
            calculator_type = request.form.get('calculatorType')
            predicted_price = predict_price_calculator(calculator_type)
            
        elif item_type == 'books':
            predicted_price = 25  # Fixed price for books
            
        print("Predicted Price:", predicted_price)  # Debug print
        return render_template('price.html', predicted_price=predicted_price)
    return render_template('price.html', predicted_price=predicted_price)
    