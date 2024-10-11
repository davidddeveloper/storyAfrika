"""
    basic functionalities to manage db, yet simple and efficient
    for a more complex operations and tweakable solution use console.py
"""
from datetime import datetime, timedelta
from models.engine import storage
from models.user import User
from models.role import Role
import sys
import os
import logging
import jwt

logging.basicConfig(filename='token.txt', level=logging.INFO)

args = sys.argv[1:]

if args[0] == 'create_superuser':
    username = str(input('Username: '))
    while username == storage._session.query(User).where(User.username == username):
        print("a user with this username already exists.")
        print("Try a different username")
        username = str(input('Username: '))

    email = str(input('Email: '))
    while '@' not in email:
        print("Invalid email address")
        email = str(input('Email: '))
    
    while email == storage._session.query(User).where(User.email == email):
        print("a user with this email already exists.")
        print("Try a different email")
        email = str(input('Email: '))
    
    password = str(input('Password: '))
    while len(password) < 3:
        print("Enter a strong password")
        password = str(input('Password: '))

    user = User(username=username, email=email, password=password)
    admin_role = storage._session.query(Role).where(Role.role == 'admin').first()
    if admin_role:
        user.roles.append(admin_role)
        user.save()
    else:
        admin_role = Role(role='admin')
        admin_role.save()
        user.roles.append(admin_role)
        user.save()
    storage.save()

if args[0] == 'load_dummy_data':
    import os
    with open('sql_scripts/storyafrika-sql') as sql_file:
        contents = sql_file.read()

        os.system(f'{contents} | sudo mysql')
    
if args[0] == 'generate_token':
    username = input('username? ')
    user = storage._session.query(User).where(User.username == username).first()
    while user is None:
        print(f'{username} does not exist.')
        username = input('username? ')
        user = storage._session.query(User).where(User.username == username).first()
    
    duration = int(input('Expiration date in (minutes)? '))
    
    # generate jwt
    payload = user.to_dict()
    payload['exp'] = (datetime.now() + timedelta(minutes=duration)).timestamp()
    
    token = jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm="HS256")
    logging.info(f"created: {datetime.now().strftime('%Y:%m:%d, %H-%M-%S')} \n{token} \nexpires: {(datetime.now() + timedelta(minutes=duration)).strftime('%Y:%m:%d, %H-%M-%S')}")
    
