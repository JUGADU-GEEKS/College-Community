from flask import Flask, Blueprint, render_template, request, session, jsonify, flash, redirect, url_for
from model import User, Product  # Make sure Product is also imported properly
from price_predict import predict_price_equipment, predict_price_calculator
from utils import notify_buyer_and_seller
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

@views.before_request
def require_login():
    if 'user' not in session:
        return redirect(url_for('auth.login'))


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/test')
def test():
    products = Product.get_all_products()
    print("📦 PRODUCTS FROM DB:", products)
    return render_template('test.html', products=products)

from flask import Blueprint, render_template, request, session, redirect, url_for
from model import Product
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['Student-Community']
users_collection = db['users']

views = Blueprint('views', __name__)

@views.route('/browse')
def browse():
    filter_by = request.args.get('filter')  # e.g. ?filter=labcoat
    print("🎯 /browse route hit with filter:", filter_by)

    raw_products = Product.get_all_products()

    items = []

    for product in raw_products:
        title = product.get("title", "").lower()
        
        # ✅ Only apply filter if it's provided
        if filter_by and filter_by.lower() not in title:
            continue

        seller_email = product.get("seller")
        seller_data = users_collection.find_one(
            {"email": seller_email}, 
            {"full_name": 1}
        )

        item = {
            "product": product,
            "seller": {
                "full_name": seller_data.get("full_name") if seller_data else "Unknown"
            }
        }
        items.append(item)

    return render_template('browse.html', items=items)



    # combined_data = []

    # for product in products:
    #     product['_id'] = str(product['_id'])
    #     product['image'] = product['image'].replace('\\', '/')

    #     seller_email = product.get('seller')
    #     print("📧 Seller Email:", seller_email)

    #     seller = User.get_data(seller_email)
    #     print("👤 Seller Data:", seller)

    #     if seller:
    #         combined_data.append({
    #             'product': product,
    #             'seller': {
    #                 'full_name': seller.get('full_name'),
    #                 'email': seller.get('email'),
    #                 'contact': seller.get('contact'),
    #                 'college': seller.get('college', ''),
    #                 'branch': seller.get('branch', ''),
    #                 'profile_photo': seller.get('profile_photo')
    #             }
    #         })

    # print("✅ FINAL combined_data:", combined_data)
    # print("🧮 Count:", len(combined_data))

    # return render_template('browse.html', items=combined_data)

@views.route('/view')
def view():
    product_id = request.args.get('id')
    # If product_id is provided, get the product from the database
    if product_id:
        product = Product.get_product_by_id(product_id)
        if product:
            seller = User.get_data(product.get('seller'))
            return render_template('view.html', product=product, seller=seller)
    
    return render_template('view.html')

@views.route('/home', methods=['POST', 'GET'])
def home():
    apron_c = Product.get_product_number_by_name('Apron')
    drafter_c = Product.get_product_number_by_name('Drafter')
    labcoat_c = Product.get_product_number_by_name('Labcoat')
    calculator_c = Product.get_product_number_by_name('Calculator')
    books_c = Product.get_product_number_by_name('Akash Books')
    return render_template('home.html', apron_c=apron_c, drafter_c=drafter_c, labcoat_c=labcoat_c, calculator_c=calculator_c, books_c=books_c)

@views.route('/profile')
def profile():
    # Check if user is logged in
    if 'user' not in session:
        return render_template('error.html', message="Please login to view your profile")
    
    # Get user information
    user_data = session.get('user')
    email = user_data.get('email')
    user = User.get_data(email)
    
    # Fetch the user's active and sold products using the product IDs stored in the user's 'bought' and 'sold' lists
    buyed_products = []
    sold_products = []
    
    # Fetch active products (not sold yet)
    for product_id in user.get('bought', []):
        product = Product.get_product_by_id(product_id)
        if product:
            buyed_products.append(product)

    # Fetch sold products
    for product_id in user.get('sold', []):
        product = Product.get_product_by_id(product_id)
        if product:
            sold_products.append(product)
    
    return render_template('profile.html', 
                          user=user,
                          buyed_products=buyed_products,
                          sold_products=sold_products)


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
            return render_template('error.html')

        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return render_template('error.html')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            print(session.get('user'))

            data = {
                'title': request.form.get('title'),
                'image': '/' + filepath,
                'description': request.form.get('description'),
                'price': request.form.get('price'),
                'monthsold': request.form.get('monthsold'),
                'condition': request.form.get('condition'),
                'seller': session.get('user').get('email')
            }
            print(data)
            product = Product(data)
            success, message = product.save_to_db()
            flash(message)
            return redirect("/browse")

        flash('Invalid file format')
        return redirect('/browse')

    # For GET request
    return render_template("browse.html")
@views.route('/about')
def about():
    return render_template('home.html', scroll_to="about")

@views.route('/contact')
def contact():
    return render_template('home.html', scroll_to="contact")
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

@views.route('/buy/<id>')
def buy(id):
    buyer = session.get('user')
    raw_product = Product.get_product_by_id(id)
    if raw_product:
        product = Product(raw_product)  # create Product instance
        seller_data = User.get_data(product.seller)
        seller_name = seller_data['full_name'] if seller_data else 'Unknown'

        if(seller_name==buyer['full_name']):
            return render_template('error.html', message="Buyer and Seller can't be same", backlink="/browse")

        return render_template('buy.html', product=product, buyer=buyer, seller_name=seller_name, id=id)
    else:
        return "Product not found", 404
    

@views.route('/purchase/<id>')
def purchase(id):
    product = Product.get_product_by_id(id)
    seller_email = product['seller']
    buyer_email = session.get('user')['email']
    buyer = User.get_data(buyer_email)
    seller = User.get_data(seller_email)
    try:
        if(seller_email==buyer_email):
            return render_template('error.html', message="Buyer and Seller can't be same", backlink="/browse")
        Product.buy_product(id, buyer['email'], seller['email'])
        notify_buyer_and_seller(buyer['email'], buyer['linkedin'], seller['email'], seller['linkedin'])
        return render_template('purchaseSuccess.html',seller_enrollment=seller['enrollment'], seller_email = seller['email'], seller_linkedin = seller['linkedin'], product = product)
    except Exception as e:
        return render_template('error.html', message=e, backlink=f'/buy/{id}')

@views.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')