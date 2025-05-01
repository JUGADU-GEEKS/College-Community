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
@views.route('/browse')
def browse():
    return render_template('browse.html')
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
            print(f'condition:{condition}')
            return render_template('addSell.html', predicted_price=int(predicted_price[0]), equipment_item=equipment_item[0].upper() + equipment_item[1:], months_old=months_old, condition=condition[0].upper()+condition[1:])

            
        elif item_type == 'calculator':
            calculator_type = request.form.get('calculatorType')
            calculator_condition = request.form.get('calculatorCondition')
            calculator_months_old = request.form.get('calculatorMonthsOld')
            calculator_demand = request.form.get('calculatorDemand')    
            predicted_price = predict_price_calculator(calculator_type, calculator_condition, int(calculator_months_old), int(calculator_demand))
            return render_template('addSell.html', predicted_price=int(predicted_price[0]), equipment_item="Calculator"+calculator_type, months_old=calculator_months_old, condition=calculator_condition[10:])

        elif item_type == 'books':
            predicted_price = 25  # Fixed price for books
            return render_template('addSell.html', predicted_price=int(predicted_price), equipment_item="Akash Books", months_old="NA", condition="NA")

    return render_template('addSell.html', predicted_price=int(predicted_price[0]))

@views.route('/test2')
def test2():
    return render_template('addSell.html')

