from flask_restx import Resource, Namespace, fields
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import( JWTManager,create_access_token, create_refresh_token,get_jwt_identity,jwt_required)
from flask import request
from exts import db  # don't forget this!

# Create auth namespace
auth_ns = Namespace('auth', description="A namespace for authentication")

# Models for Swagger (API docs)
signup_model = auth_ns.model(
    'SignUp',
    {
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True)
    }
)

login_model = auth_ns.model(
    'Login',
    {
        "username": fields.String(required=True),
        "password": fields.String(required=True)
    }
)

# -------------------- Routes --------------------

@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        db_user = User.query.filter_by(username=username).first()
        if db_user is not None:
            return {"message": f"User with username '{username}' already exists"}, 400

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return {"message": f"User '{username}' created successfully!"}, 201


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.username)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        else:
            return {"message": "Invalid username or password"}, 401

@auth_ns.route('/refresh')
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):

        current_user=get_jwt_identity()
        new_access_token=create_access_token(identity=current_user)

        return {"access_token": new_access_token}, 200

