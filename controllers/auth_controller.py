from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, user_schema, users_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def auth_register():
  try:
    # {"name": "User User2","email": "user2@email.com", "password": "user2pw"} from postman 
    body_data = request.get_json()

    #ceate a new user model instance from the user info
    user = User() # Instance of the User class which is in turn a SQLAlchemy model 
    user.name = body_data.get('name')
    user.email = body_data.get('email')
    if body_data.get('password'):
      user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
    # Add the user to the session
    db.session.add(user)
    # Commit to add the user to the database
    db.session.commit()
    # Respond to the client
    return user_schema.dump(user), 201
  except IntegrityError as err:
    if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
      return { 'error': "Email address is already in use" }, 409
    if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
      return { 'error': f'The {err.orig.diag.column_name} is required' }, 409

@auth_bp.route('/login', methods=['POST'])
def auth_login():
    body_data = request.get_json()
    # Find the user by email address
    stmt = db.select(User).filter_by(email=body_data.get('email'))
    user = db.session.scalar(stmt)
    # If user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get('password')):
      token = create_access_token(identity=str(user.id))
      return { 'email': user.email, 'token': token, 'is_admin': user.is_admin }
    else:
      return { 'error': 'Invalid email or password' }, 401
    