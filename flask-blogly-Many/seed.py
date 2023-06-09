from models import db, User
from app import app

db.drop_all()
db.create_all()

User.query.delete()

# Add Users
# Create a list of dictionaries with the data for each user
users_data = [
    {'first_name': 'John', 'last_name': 'Doe', 'image_url': 'https://www.freeiconspng.com/uploads/person-icon-user-person-man-icon-1.png'},
    {'first_name': 'Jane', 'last_name': 'Doe', 'image_url': 'https://www.freeiconspng.com/uploads/person-icon-user-person-man-icon-2.png'},
    {'first_name': 'Alice', 'last_name': 'Smith', 'image_url': 'https://www.freeiconspng.com/uploads/person-icon-user-person-man-icon-3.png'},
    {'first_name': 'Bob', 'last_name': 'Johnson', 'image_url': 'https://www.freeiconspng.com/uploads/person-icon-user-person-man-icon-4.png'},
    {'first_name': 'Charlie', 'last_name': 'Brown', 'image_url': 'https://www.freeiconspng.com/uploads/person-icon-user-person-man-icon-5.png'},
    {'first_name': 'Diana', 'last_name': 'Ross', 'image_url': 'https://www.freeiconspng.com/uploads/person-icon-user-person-man-icon-6.png'},
    {'first_name': 'Ethan', 'last_name': 'Hunt', 'image_url': 'https://www.freeiconspng.com/uploads/person-icon-user-person-man-icon-7.png'},
    {'first_name': 'Fiona', 'last_name': 'Apple', 'image_url': 'https://www.freeiconspng.com/uploads/person-icon-user-person-man-icon-8.png'},
    {'first_name': 'George', 'last_name': 'Washington', 'image_url': 'https://www.freeiconspng.com/uploads/person-icon-user-person-man-icon-9.png'},
    {'first_name': 'Helen', 'last_name': 'Mirren', 'image_url': 'https://www.freeiconspng.com/uploads/person-icon-user-person-man-icon-10.png'},
]

# Loop over the list and create a new User object for each one
for user_data in users_data:
    user = User(first_name=user_data['first_name'], last_name=user_data['last_name'], image_url=user_data['image_url'])
    db.session.add(user)

# Commit the session to insert the new users
db.session.commit()
