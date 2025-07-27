# Utility function to get college name by user email
from pymongo import MongoClient
import os
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['Student-Community']
users_collection = db['users']

def get_college_by_email(email):
    user = users_collection.find_one({"email": email})
    if user:
        return user.get('college', None)
    return None
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId  # Ensure this import is at the top
import datetime


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
print(f"Loaded MONGO_URI: {MONGO_URI}")
client = MongoClient(MONGO_URI)
db = client['Student-Community']
users_collection = db['users']
products_collection = db['products']

class User:
    def __init__(self, data):
        self.full_name = data.get('full_name')
        self.enrollment = data.get('enrollment')
        self.email = data.get('email')
        self.contact = data.get('contact')
        self.college = data.get('college')
        self.course = data.get('course')
        self.branch = data.get('branch')
        self.section = data.get('section')
        self.password = generate_password_hash(data.get('password'))
        self.profile_photo = 'https://unsplash.com/photos/woman-with-dslr-camera-e616t35Vbeg'
        self.otp = None
        self.linkedin = data.get('linkedin')
        self.isVerified = False
        # New lists for tracking product relations
        self.bought = []  # product _id values of bought items
        self.sold = []    # product _id values of sold items

    def save_to_db(self):
        if users_collection.find_one({"email": self.email}):
            return False, "Email already exists!"
        users_collection.insert_one(self.__dict__)
        return True, "Account created! Please verify your email."

    @staticmethod
    def verify_user(email, otp):
        user = users_collection.find_one({"email": email})
        if user and user['otp'] == otp:
            users_collection.update_one({"email": email}, {"$set": {"isVerified": True}})
            return True
        return False

    @staticmethod
    def check_password(email, password):
        user = users_collection.find_one({"email": email})
        return user and check_password_hash(user['password'], password)
    
    def upload_image(self, image_address):
        self.profile_photo = image_address

    @staticmethod
    def get_data(email):
        return users_collection.find_one({"email": email})
    
    def update_otp(self, otp):
        self.otp = otp
        users_collection.update_one({"email": self.email}, {"$set": {"otp": otp}})

    @staticmethod
    def update_password(email, password):
        users_collection.update_one({"email": email}, {"$set": {"password": generate_password_hash(password)}})

class Product:
    def __init__(self, data):
        self.title = data.get('title')
        self.image = data.get('image')
        self.description = data.get('description')
        self.price = data.get('price')
        self.monthsold = data.get('monthsold')
        self.condition = data.get('condition')
        self.isSold = False
        self.seller = data.get('seller')
        self.buyer = None
        self.payment = 'Pending'
        self.status = data.get('status', 'pending')  # New field for approval status
        self.college = get_college_by_email(data.get('seller'))

    def save_to_db(self):
        # Step 1: Insert the product and get the inserted ID
        result = products_collection.insert_one(self.__dict__)
        product_id = result.inserted_id

        # Step 2: Push the product_id to the seller's 'sold' list
        users_collection.update_one(
            {"email": self.seller},
            {"$push": {"sold": product_id}}
        )

        return True, "Product added successfully!"

    @staticmethod
    def get_all_products():
        # Only return products that are not sold and are approved
        return list(products_collection.find({"isSold": False, "status": "approved"}))

    

    @staticmethod
    def buy_product(product_id, buyer_email, seller_email):
        try:
            result = products_collection.update_one(
                {"_id": ObjectId(product_id), "isSold": False},
                {"$set": {"isSold": True, "buyer": buyer_email}}
            )

            if result.modified_count > 0:
                users_collection.update_one(
                    {"email": buyer_email},
                    {"$push": {"bought": product_id}}
                )
                users_collection.update_one(
                    {"email": seller_email},
                    {"$push": {"sold": product_id}}
                )
                return True
            return False
        except Exception as e:
            print("Error in buy_product:", e)
            return False

    
    @staticmethod
    def get_product_by_id(product_id):
        try:
            return products_collection.find_one({"_id": ObjectId(product_id)})
        except Exception:
            return None
        
    @staticmethod
    def get_product_number_by_name(name):
        try:
            if name.lower() == 'calculator':
                return products_collection.count_documents({
                    "title": {"$regex": "calculator", "$options": "i"}, # case-insensitive
                    "isSold": False  
                })
            return products_collection.count_documents({"title": name, "isSold": False})
        except Exception:
            return 0
        
    def to_dict(self):
        return {
            "title": self.title,
            "image": self.image,
            "description": self.description,
            "price": self.price,
            "monthsold": self.monthsold,
            "condition": self.condition,
            "isSold": self.isSold,
            "seller": self.seller,
            "buyer": self.buyer
        }


class Purchase:
    
    def __init__(self, data):
        self.product_id = data.get('product_id')
        self.seller_name = data.get('seller_name')
        self.buyer_name = data.get('buyer_name')
        self.seller_contact = data.get('seller_contact')
        self.buyer_contact = data.get('buyer_contact')
        self.seller_email = data.get('seller_email')
        self.buyer_email = data.get('buyer_email')
        self.selling_price = data.get('selling_price')
        self.buying_price = data.get('buying_price')
        self.payment_status = data.get('payment_status', 'Pending')
        self.created_at = data.get('created_at', datetime.datetime.utcnow())
        self.college = get_college_by_email(data.get('seller_email'))

    def save_to_db(self):
        purchase_data = {
            'product_id': self.product_id,
            'seller_name': self.seller_name,
            'buyer_name': self.buyer_name,
            'seller_contact': self.seller_contact,
            'buyer_contact': self.buyer_contact,
            'seller_email': self.seller_email,
            'buyer_email': self.buyer_email,
            'selling_price': self.selling_price,
            'buying_price': self.buying_price,
            'payment_status': self.payment_status,
            'created_at': self.created_at,
            'college': self.college
        }
        db['purchases'].insert_one(purchase_data)
        return True, "Purchase recorded successfully!"

    @staticmethod
    def get_all_purchases():
        return list(db['purchases'].find())

class FaultyBuyer:
    def __init__(self, email):
        self.email = email

    @staticmethod
    def increment_fault(email):
        db['faulty_buyers'].update_one(
            {'email': email},
            {'$inc': {'fault_count': 1}},
            upsert=True
        )
        # Check if fault count exceeds 7
        record = db['faulty_buyers'].find_one({'email': email})
        if record and record.get('fault_count', 0) > 7:
            # Terminate account
            db['users'].delete_one({'email': email})
            return True  # Account terminated
        return False

    @staticmethod
    def get_fault_count(email):
        record = db['faulty_buyers'].find_one({'email': email})
        return record.get('fault_count', 0) if record else 0

    @staticmethod
    def get_all_faulty_buyers():
        return list(db['faulty_buyers'].find())

    @staticmethod
    def update_fault_count(email, count):
        db['faulty_buyers'].update_one(
            {'email': email},
            {'$set': {'fault_count': count}},
            upsert=True
        )