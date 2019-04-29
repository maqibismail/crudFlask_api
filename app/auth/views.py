from . import auth_blueprint
from flask_restful import reqparse
from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User
from . import urls

class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True)
        args = parser.parse_args()
        try: 
            user = User.query.filter_by(email=args['email']).first()
            
            if not user:
                try:
                    parser = reqparse.RequestParser()
                    parser.add_argument('email', required=True)
                    parser.add_argument('password', required=True)

                    args2 = parser.parse_args()
                    email = args2['email']
                    password = args2['password']
                    user = User(email=email, password=password)
                    user.save()
                    response = {
                        'message': 'You registered successfully. Please log in.'
                    }
                    return make_response(jsonify(response)), 201
                except Exception as e:
                    response = {'message': str(e)}
                    return make_response(jsonify(response)), 401
            else:
                response = {
                    'message': 'User already exists. Please login.'
                }
                return make_response(jsonify(response)), 202
        except Exception as error:
            return("Error", error)

class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        try:
            
            parser = reqparse.RequestParser()
            parser.add_argument('email', required=True)
            parser.add_argument('password', required=True)
            args = parser.parse_args()
           
            user = User.query.filter_by(email=args['email']).first()
      
            if user and user.password_is_valid(args['password']):
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'message': 'Invalid email or password, Please try again'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:
            response = {
                'message ': str(e)
            }
            return make_response(jsonify(response)), 500