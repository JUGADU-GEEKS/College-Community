from flask import Flask, Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
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
    # Get filter parameters
    category = request.args.get('category', 'all')
    condition = request.args.get('condition')
    max_price = request.args.get('max_price')
    
    # Get all categories for the filter dropdown
    categories = {'all': 'All Products', 'drafter': 'Drafters', 'lab_apron': 'Lab Aprons', 'sheet_holder': 'Sheet Holders', 'calculator': 'Calculators'}
    
    # In the real implementation, you would get filtered products from the database
    # For now, empty products list as a placeholder
    products = []
    
    return render_template('browse.html', 
                          products=products, 
                          categories=categories, 
                          selected_category=category, 
                          selected_condition=condition, 
                          selected_max_price=max_price)

@views.route('/view')
def view():
    product_id = request.args.get('id')
    # In the real implementation, you would get the product from the database
    # For now, return error page
    return render_template('error.html', message="Product not found")

@views.route('/home', methods=['POST','GET'])
def home():
    # Get all categories for the filter section
    categories = {'all': 'All Products', 'drafter': 'Drafters', 'lab_apron': 'Lab Aprons', 'sheet_holder': 'Sheet Holders', 'calculator': 'Calculators'}
    
    # Get filter parameters
    category = request.args.get('category', 'all')
    condition = request.args.get('condition')
    max_price = request.args.get('max_price')
    
    # In the real implementation, you would get filtered products from the database
    # For now, empty products list as a placeholder
    products = []
    
    return render_template('home.html', 
                          products=products, 
                          categories=categories,
                          selected_category=category,
                          selected_condition=condition,
                          selected_max_price=max_price)

@views.route('/profile')
def profile():
    # Check if user is logged in
    if 'user' not in session:
        return render_template('error.html', message="Please login to view your profile")
    
    # Get user information
    user_data = session.get('user')
    email = user_data.get('email')
    user = User.get_data(email)
    
    # In a real implementation, you would fetch the user's active and sold products
    # For now, we'll use empty lists as placeholders
    active_products = []
    sold_products = []
    
    return render_template('profile.html', 
                          user=user,
                          active_products=active_products,
                          sold_products=sold_products)

@views.route('/sell',methods=['POST','GET'])
def sell():
    # Get categories for dropdowns
    categories = {'all': 'All Products', 'drafter': 'Drafters', 'lab_apron': 'Lab Aprons', 'sheet_holder': 'Sheet Holders', 'calculator': 'Calculators'}
    return render_template('sell.html', categories=categories)

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

    return render_template('addSell.html', predicted_price=25)  # Default value for GET request

@views.route('/test2')
def test2():
    return render_template('addSell.html')

@views.route('/about')
def about():
    return render_template('home.html', scroll_to="about")

@views.route('/contact')
def contact():
    return render_template('home.html', scroll_to="contact")

# API endpoint for AJAX product filtering
@views.route('/api/products', methods=['GET'])
def api_products():
    category = request.args.get('category', 'all')
    condition = request.args.get('condition')
    max_price = request.args.get('max_price')
    
    # In a real implementation, you would get filtered products from the database
    # For now, return empty list
    products = []
    return jsonify({'products': products})

@views.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'user' not in session:
        flash('You must be logged in to update your avatar.', 'danger')
        return redirect(url_for('views.profile'))

    user_data = session.get('user')
    email = user_data.get('email')
    user = User.get_data(email)

    avatar_url = request.form.get('avatar_url')
    avatar_file = request.files.get('avatar_file')
    new_avatar_url = None

    # If a preset avatar is selected
    if avatar_url:
        new_avatar_url = avatar_url
    # If a file is uploaded
    elif avatar_file and avatar_file.filename:
        filename = secure_filename(avatar_file.filename)
        avatar_folder = os.path.join('static', 'avatars')
        os.makedirs(avatar_folder, exist_ok=True)
        file_path = os.path.join(avatar_folder, filename)
        avatar_file.save(file_path)
        new_avatar_url = '/' + file_path.replace('\\', '/').replace(os.path.sep, '/')

    if new_avatar_url:
        # Update in DB
        from pymongo import MongoClient
        MONGO_URI = os.getenv("MONGO_URI")
        client = MongoClient(MONGO_URI)
        db = client['Student-Community']
        users_collection = db['users']
        users_collection.update_one({"email": email}, {"$set": {"profile_photo": new_avatar_url}})
        # Also update session
        session['user']['profile_photo'] = new_avatar_url
        flash('Avatar updated successfully!', 'success')
    else:
        flash('Please select or upload an avatar.', 'warning')

    return redirect(url_for('views.profile'))

