import bcrypt

password = "adminofthestuddybuddyy69283123"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

print(hashed.decode())  # This will give a string to store in .env


import cloudinary
import cloudinary.uploader

cloudinary.config( 
  cloud_name = "dwbgl0h17", 
  api_key = "126572313438464", 
  api_secret = "v-LXJgv3TZ1Fsm09QgOv3uh2gFA" 
)

result = cloudinary.uploader.upload("./static/avatars/image.png")
print(result["secure_url"])