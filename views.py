from flask import Flask, Blueprint, render_template, request, session, jsonify, flash, redirect, url_for, send_file
from model import User, Product, Purchase, FaultyBuyer  # Make sure Product and Purchase are also imported properly
from price_predict import predict_price_equipment, predict_price_calculator
from utils import notify_buyer_and_seller, send_otp, send_faulty_buyer_warning, build_html_email, EMAIL_USER, EMAIL_PASS, WEBSITE_NAME
import os
from email.message import EmailMessage
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
import smtplib
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


views = Blueprint('views', __name__)

@views.before_request
def require_login():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

@views.before_request
def require_college():
    allowed_routes = ['views.landing','static']
    # If user is logged in and has a token, allow navigation
    if session.get('user') and session.get('token'):
        return None
    if request.endpoint not in allowed_routes and not session.get('college_name'):
        return redirect(url_for('views.welcome'))


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



MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['Student-Community']
users_collection = db['users']

views = Blueprint('views', __name__)




# Default landing page route
@views.route('/')
def landing():
    return render_template('landing.html')

# Route to handle college selection from landing page
@views.route('/select_college', methods=['POST'])
def select_college():
    college_name = request.form.get('college_name')
    if not college_name:
        return redirect(url_for('views.landing'))
    # Store selected college in session
    session['selected_college'] = college_name
    return redirect(url_for('views.browse_college', college_name=college_name))

# Browse page filtered by selected college, all buttons redirect to welcome
@views.route('/browse_college')
def browse_college():
    from model import get_college_by_email
    college_name = request.args.get('college_name') or session.get('selected_college')
    if not college_name:
        return redirect(url_for('views.landing'))
    raw_products = Product.get_all_products()
    items = []
    for product in raw_products:
        seller_email = product.get("seller")
        seller_college = get_college_by_email(seller_email)
        if not seller_college:
            continue
        if seller_college.strip().lower() != college_name.strip().lower():
            continue
        seller_data = users_collection.find_one({"email": seller_email})
        item = {
            "product": product,
            "seller": {
                "full_name": seller_data.get("full_name") if seller_data else "Unknown"
            }
        }
        items.append(item)
    return render_template('browse_college.html', items=items, college_name=college_name)
@views.route('/welcome')
def welcome():
    return render_template('welcome.html')

@views.route('/browse')
def browse():
    # Require login for /sell
    # if 'user' not in session:
    #     return redirect(url_for('auth.login'))
    from model import get_college_by_email
    filter_by = request.args.get('filter')
    user_data = session.get('user')
    if not user_data:
        return redirect(url_for('auth.login'))
    current_user_email = user_data.get('email')
    college_name = get_college_by_email(current_user_email)
    raw_products = Product.get_all_products()
    items = []
    for product in raw_products:
        title = product.get("title", "").lower()
        seller_email = product.get("seller")
        if filter_by and filter_by.lower() not in title:
            continue
        if seller_email == current_user_email:
            continue
        seller_college = get_college_by_email(seller_email)
        if not seller_college or not college_name:
            continue
        if seller_college.strip().lower() != college_name.strip().lower():
            continue
        seller_data = users_collection.find_one({"email": seller_email})
        item = {
            "product": product,
            "seller": {
                "full_name": seller_data.get("full_name") if seller_data else "Unknown"
            }
        }
        items.append(item)
    return render_template('browse.html', items=items, college_name=college_name)

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
    user_data = session.get('user')
    user = None
    if user_data:
        email = user_data.get('email')
        user = User.get_data(email)
    return render_template('home.html', apron_c=apron_c, drafter_c=drafter_c, labcoat_c=labcoat_c, calculator_c=calculator_c, books_c=books_c, sheet_c=sheet_c, user=user)

@views.route('/profile')
def profile():
    # Check if user is logged in
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
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
    # Require login for /sell
    # if 'user' not in session:
    #     return redirect(url_for('auth.login'))
    return render_template('sell.html')

@views.route('/price', methods=['POST', 'GET'])
def price():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
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

        if file and allowed_file(file.filename):  # Assuming you already have this function
            # Upload to Cloudinary instead of saving locally
            upload_result = cloudinary.uploader.upload(file)

            print(session.get('user'))

            data = {
                'title': request.form.get('title'),
                'image': upload_result.get('secure_url'),  # Cloudinary image URL
                'description': request.form.get('description'),
                'price': request.form.get('price'),
                'monthsold': request.form.get('monthsold'),
                'condition': request.form.get('condition'),
                'seller': session.get('user').get('email'),
                'status': 'pending'  # Set status to pending for admin approval
            }

            print(data)
            product = Product(data)
            success, message = product.save_to_db()
            # Send product submission email
            from utils import send_product_submission_email
            send_product_submission_email(data['seller'], data['title'])
            flash('Product submitted for admin approval!')
            return redirect('/sell')

        flash('Invalid file format')
        return redirect('/addSell')

    return render_template('addSell.html')

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

@views.route('/upload_cover', methods=['POST'])
def upload_cover():
    if 'user' not in session:
        flash('You must be logged in to update your cover image.', 'danger')
        return redirect(url_for('views.profile'))

    user_data = session.get('user')
    email = user_data.get('email')
    user = User.get_data(email)

    cover_url = request.form.get('cover_url')
    new_cover_url = None

    # Only preset cover images for now
    if cover_url:
        new_cover_url = cover_url

    if new_cover_url:
        from pymongo import MongoClient
        MONGO_URI = os.getenv("MONGO_URI")
        client = MongoClient(MONGO_URI)
        db = client['Student-Community']
        users_collection = db['users']
        users_collection.update_one({"email": email}, {"$set": {"cover_image": new_cover_url}})
        # Also update session
        session['user']['cover_image'] = new_cover_url
        flash('Cover image updated successfully!', 'success')
    else:
        flash('Please select a cover image.', 'warning')

    return redirect(url_for('views.profile'))

@views.route('/buy/<id>')
def buy(id):
    buyer = session.get('user')
    raw_product = Product.get_product_by_id(id)
    if raw_product:
        product = Product(raw_product)  # create Product instance
        seller_data = User.get_data(product.seller)
        seller_name = seller_data['full_name'] if seller_data else 'Unknown'
        college_name = seller_data['college']

        if(seller_name==buyer['full_name']):
            return render_template('error.html', message="Buyer and Seller can't be same", backlink="/browse")

        return render_template('buy.html', product=product, buyer=buyer, seller_name=seller_name, id=id, college_name=college_name)
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
        # Prevent duplicate purchase on reload
        existing_purchase = db['purchases'].find_one({'product_id': str(product['_id']), 'buyer_email': buyer_email})
        if existing_purchase:
            purchase_id = str(existing_purchase['_id'])
            return render_template('purchaseSuccess.html', purchase_id=purchase_id, product=product)
        Product.buy_product(id, buyer['email'], seller['email'])
        notify_buyer_and_seller(buyer['email'], seller['email'])


        # Determine buying price based on seller's college
        price = int(product.get('price'))
        seller_college = seller.get('college').strip()

        if seller_college == 'Delhi Technological University':
            buying_price = price + 7
        else:
            buying_price = price + 30

        # Save purchase record
        purchase_data = {
            'product_id': str(product['_id']),
            'seller_name': seller.get('full_name'),
            'buyer_name': buyer.get('full_name'),
            'seller_contact': seller.get('contact'),
            'buyer_contact': buyer.get('contact'),
            'seller_email': seller.get('email'),
            'buyer_email': buyer.get('email'),
            'selling_price': price,
            'buying_price': buying_price,
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
                'college' : user.get('college'),
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
    if 'user' not in session:
        return redirect(url_for('auth.admin_login'))

    college = session['user'].get('college')
    print(f"The college set is :{college}")

    from model import Purchase
    purchases = Purchase.get_all_purchases()
    now = datetime.datetime.utcnow()
    filtered_purchases = []

    for p in purchases:
        print(f"The college get is :{p.get(college)}")
        if p.get('payment_status') == 'Success' and p.get('college') == college:
            
            created_at = p.get('created_at')
            if created_at is None:
                filtered_purchases.append(p)
            else:
                if isinstance(created_at, str):
                    try:
                        created_at = datetime.datetime.fromisoformat(created_at)
                    except Exception:
                        filtered_purchases.append(p)
                        continue
                if (now - created_at).days <= 30:
                    filtered_purchases.append(p)
        elif p.get('payment_status') != 'Success' and p.get('college') == college:
            filtered_purchases.append(p)

    pending_products = list(db['products'].find({'status': 'pending', 'college': college}))
    return render_template('adminDashboard.html', purchases=filtered_purchases, pending_products=pending_products)

@views.route('/admin/approve_product/<product_id>', methods=['POST'])
def approve_product(product_id):
    db['products'].update_one({'_id': ObjectId(product_id)}, {'$set': {'status': 'approved'}})
    # Fetch product details for email
    product = db['products'].find_one({'_id': ObjectId(product_id)})
    if product:
        seller_email = product.get('seller')
        product_title = product.get('title')
        from utils import send_product_approval_email
        send_product_approval_email(seller_email, product_title)
    flash('Product approved and now visible in browse!')
    return redirect(url_for('views.admin_dashboard'))

@views.route('/admin/reject_product/<product_id>', methods=['POST'])
def reject_product(product_id):
    db['products'].update_one({'_id': ObjectId(product_id)}, {'$set': {'status': 'rejected'}})
    # Fetch product details for email
    product = db['products'].find_one({'_id': ObjectId(product_id)})
    if product:
        seller_email = product.get('seller')
        product_title = product.get('title')
        from utils import send_product_rejection_email
        send_product_rejection_email(seller_email, product_title)
    flash('Product rejected!')
    return redirect(url_for('views.admin_dashboard'))

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
    # Fetch product and seller info
    product = db['products'].find_one({'_id': ObjectId(product_id)})
    seller_email = product.get('seller') if product else None
    # Send payment success emails to both buyer and seller
    if product and seller_email:
        from utils import send_payment_success_emails
        send_payment_success_emails(buyer_email, seller_email, product)
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

@views.route('/payment_received/<product_id>/<buyer_email>', methods=['POST'])
def payment_received(product_id, buyer_email):
    from model import Purchase, User, Product
    import traceback
    # Find the purchase record
    purchase = next((p for p in Purchase.get_all_purchases() if str(p.get('product_id')) == str(product_id) and p.get('buyer_email') == buyer_email), None)
    if not purchase:
        return "Purchase not found", 404

    # Get buyer info
    buyer = User.get_data(buyer_email)
    if not buyer:
        return "Buyer not found", 404

    # Compose and send the payment received email
    subject = f"{WEBSITE_NAME} - Payment Received Confirmation"
    heading = "Payment Received!"
    message = f"Dear {buyer.get('full_name', 'Buyer')},<br><br>We have received your payment for your recent purchase. We will be giving you the product soon!<br><br>Thank you for shopping with us!"
    action_url = "http://localhost:5000/profile"
    action_text = "View Your Profile"

    # Load email credentials fresh from environment
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASS = os.getenv('EMAIL_PASS')
    print('EMAIL_USER used:', EMAIL_USER)
    print('EMAIL_PASS used:', EMAIL_PASS)

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = buyer_email
    msg.set_content("We have received your payment. Thank you!")
    msg.add_alternative(build_html_email(subject, heading, message, action_url=action_url, action_text=action_text), subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
    except Exception as e:
        print('Failed to send payment received email:', e)
        print('Traceback:', traceback.format_exc())
        return render_template('error.html', message=f'Failed to send email: {e}')

    return redirect('/adminDashboard')

@views.route('/sitemap.xml')
def sitemap():
    return send_file('sitemap.xml')