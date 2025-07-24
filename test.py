import bcrypt

password = "adminofthestuddybuddyy69283123"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

print(hashed.decode())  # This will give a string to store in .env
