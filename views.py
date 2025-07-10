from flask import Flask, Blueprint, render_template, request, session, jsonify, flash, redirect, url_for
from model import User, Product, Purchase, FaultyBuyer  # Make sure Product and Purchase are also imported properly
from price_predict import predict_price_equipment, predict_price_calculator
from utils import notify_buyer_and_seller, send_otp, send_faulty_buyer_warning
import os
from email.message import EmailMessage
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId

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
    current_user_email = session.get('user', {}).get('email')

    for product in raw_products:
        title = product.get("title", "").lower()
        # Only apply filter if it's provided
        if filter_by and filter_by.lower() not in title:
            continue
        seller_email = product.get("seller")
        # Skip products listed by the current user
        if seller_email == current_user_email:
            continue
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
    sheet_c = Product.get_product_number_by_name('Sheetholder')
    return render_template('home.html', apron_c=apron_c, drafter_c=drafter_c, labcoat_c=labcoat_c, calculator_c=calculator_c, books_c=books_c, sheet_c=sheet_c)

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
        notify_buyer_and_seller(buyer['email'], buyer.get('linkedin'), seller['email'], seller.get('linkedin'))

        # Save purchase record
        purchase_data = {
            'product_id': str(product['_id']),
            'seller_name': seller.get('full_name'),
            'buyer_name': buyer.get('full_name'),
            'seller_contact': seller.get('contact'),
            'buyer_contact': buyer.get('contact'),
            'seller_email': seller.get('email'),
            'buyer_email': buyer.get('email'),
            'selling_price': product.get('price'),
            'buying_price': int(product.get('price')) + 30,  # Assuming same as selling price
            'payment_status': product.get('payment', 'Pending')
        }
        purchase_record = Purchase(purchase_data)
        result = purchase_record.save_to_db()
        # Get the inserted purchase_id
        if hasattr(result, 'inserted_id'):
            purchase_id = str(result.inserted_id)
        elif isinstance(result, tuple) and hasattr(result[0], 'inserted_id'):
            purchase_id = str(result[0].inserted_id)
        else:
            # fallback: try to get the last inserted purchase
            last_purchase = db['purchases'].find_one(sort=[('_id', -1)])
            purchase_id = str(last_purchase['_id']) if last_purchase else 'N/A'

        return render_template('purchaseSuccess.html', purchase_id=purchase_id, product=product)
    except Exception as e:
        return render_template('error.html', message=e, backlink=f'/buy/{id}')

@views.route('/leaderboard')
def leaderboard():
    from model import Purchase, User
    from collections import Counter
    # Get all purchases with payment_status == 'Success'
    purchases = Purchase.get_all_purchases()
    success_purchases = [p for p in purchases if p.get('payment_status') == 'Success']

    # Count successful purchases per buyer and seller
    buyer_counter = Counter()
    seller_counter = Counter()
    for p in success_purchases:
        buyer_counter[p.get('buyer_email')] += 1
        seller_counter[p.get('seller_email')] += 1

    # Get top 10 buyers and sellers
    top_buyers = buyer_counter.most_common(10)
    top_sellers = seller_counter.most_common(10)

    # Fetch user info for leaderboard display
    def get_user_info(email, count):
        user = User.get_data(email)
        if user:
            return {
                'full_name': user.get('full_name', 'Unknown'),
                'email': email,
                'profile_photo': user.get('profile_photo', '/static/avatars/image.png'),
                'linkedin': user.get('linkedin', None),
                'count': count
            }
        else:
            return {
                'full_name': 'Unknown',
                'email': email,
                'profile_photo': '/static/avatars/image.png',
                'linkedin': None,
                'count': count
            }

    leaderboard_buyers = [get_user_info(email, count) for email, count in top_buyers]
    leaderboard_sellers = [get_user_info(email, count) for email, count in top_sellers]

    return render_template('leaderboard.html', buyers=leaderboard_buyers, sellers=leaderboard_sellers)

@views.route('/adminDashboard')
def admin_dashboard():
    from model import Purchase
    purchases = Purchase.get_all_purchases()
    return render_template('adminDashboard.html', purchases=purchases)

@views.route('/faulty_buyer/<product_id>/<buyer_email>', methods=['POST'])
def mark_faulty_buyer(product_id, buyer_email):
    # Set product isSold to False and buyer to None
    db['products'].update_one(
        {'_id': ObjectId(product_id)},
        {'$set': {'isSold': False, 'buyer': None}}
    )
    # Increment fault count and terminate if needed
    terminated = FaultyBuyer.increment_fault(buyer_email)
    # Get current fault count
    fault_count = FaultyBuyer.get_fault_count(buyer_email)
    # Delete the purchase from the purchases collection
    db['purchases'].delete_one({'product_id': product_id, 'buyer_email': buyer_email})
    # Send email to buyer using utility function
    send_faulty_buyer_warning(buyer_email, fault_count)
    return redirect(url_for('views.admin_dashboard'))

@views.route('/set_payment_success/<product_id>/<buyer_email>', methods=['POST'])
def set_payment_success(product_id, buyer_email):
    # Update payment status in purchases collection
    db['purchases'].update_one(
        {'product_id': product_id, 'buyer_email': buyer_email},
        {'$set': {'payment_status': 'Success'}}
    )
    # Update payment status in products collection
    db['products'].update_one(
        {'_id': ObjectId(product_id)},
        {'$set': {'payment': 'Success'}}
    )
    return redirect(url_for('views.admin_dashboard'))

@views.route('/faulty_buyers', methods=['GET', 'POST'])
def faulty_buyers():
    from model import FaultyBuyer
    if request.method == 'POST':
        email = request.form.get('email')
        count = int(request.form.get('count'))
        FaultyBuyer.update_fault_count(email, count)
        return redirect(url_for('views.faulty_buyers'))
    buyers = FaultyBuyer.get_all_faulty_buyers()
    return render_template('faultyBuyers.html', buyers=buyers)

@views.route('/notes')
def notes():
    return render_template('notes.html')

