from flask import Flask, Blueprint, render_template, request, session, jsonify, flash, redirect, url_for
from model import User, Product  # Make sure Product is also imported properly
from price_predict import predict_price_equipment, predict_price_calculator
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    products = Product.get_all_products()
    combined_data = []

    for product in products:
        seller_email = product.get('seller')
        seller = User.get_data(seller_email)
        if seller:
            combined_data.append({
                'product': product,
                'seller': {
                    'full_name': seller.get('full_name'),
                    'email': seller.get('email'),
                    'contact': seller.get('contact'),
                    'college': seller.get('college'),
                    'branch': seller.get('branch'),
                    'profile_photo': seller.get('profile_photo')
                }
            })

    return render_template('browse.html', items=combined_data)

@views.route('/view')
def view():
    return render_template('view.html')

@views.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

@views.route('/sell', methods=['POST', 'GET'])
def sell():
    return render_template('sell.html')

@views.route('/price', methods=['POST', 'GET'])
def price():
    predicted_price = None
    if request.method == 'POST':
        item_type = request.form.get('itemType')
        if item_type == 'equipment':
            equipment_item = request.form.get('equipmentItem')
            months_old = request.form.get('monthsOld')
            condition = request.form.get('condition')
            predicted_price = predict_price_equipment(equipment_item, int(months_old), condition)
            return render_template('addSell.html', predicted_price=int(predicted_price[0]),
                                   equipment_item=equipment_item.capitalize(), months_old=months_old,
                                   condition=condition.capitalize())

        elif item_type == 'calculator':
            calculator_type = request.form.get('calculatorType')
            calculator_condition = request.form.get('calculatorCondition')
            calculator_months_old = request.form.get('calculatorMonthsOld')
            calculator_demand = request.form.get('calculatorDemand')
            predicted_price = predict_price_calculator(calculator_type, calculator_condition,
                                                       int(calculator_months_old), int(calculator_demand))
            return render_template('addSell.html', predicted_price=int(predicted_price[0]),
                                   equipment_item="Calculator " + calculator_type, months_old=calculator_months_old,
                                   condition=calculator_condition[10:])

        elif item_type == 'books':
            predicted_price = 25
            return render_template('addSell.html', predicted_price=predicted_price,
                                   equipment_item="Akash Books", months_old="NA", condition="NA")

    return render_template('addSell.html', predicted_price=0)
@views.route('/addProduct', methods=['GET', 'POST'])
def addProduct():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No image part')
            return redirect(request.url)

        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            data = {
                'title': request.form.get('title'),
                'image': '/' + filepath,
                'description': request.form.get('description'),
                'price': request.form.get('price'),
                'monthsold': request.form.get('monthsold'),
                'condition': request.form.get('condition'),
                'selleremail': session.get('user').get('email')
            }
            print(data)
            product = Product(data)
            success, message = product.save_to_db()
            flash(message)
            return render_template('test.html', method="Post")  # Update as needed

        flash('Invalid file format')
        return redirect(request.url)

    # For GET request
    return render_template("test.html", method="GET")
