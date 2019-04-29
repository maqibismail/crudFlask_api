from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_api import FlaskAPI
from .models import Candidate, User
from flask.views import MethodView
from flask import make_response, request, jsonify
from flask_restful import reqparse
from . import candidate_blueprint
from uuid import UUID
import os, base64
import uuid
from . import create_app
from . import urls
from instance.config import app_config

candidate = ''
db = SQLAlchemy()
class crud_candidateView(MethodView):
        @candidate_blueprint.before_request
        def before_request():
            parser = reqparse.RequestParser()
            parser.add_argument('enrolement_no')
            args = parser.parse_args()

            if args.get('enrolement_no'):
                try:
                    global candidate
                    valid_enrolement_no = str(UUID(args['enrolement_no']))    ## check valid enrolement number
                    if valid_enrolement_no:
                        candidate = Candidate.query.filter_by(enrolement_no=args['enrolement_no']).first()
                        if not candidate:
                            return make_response("No candidate found", 404)
                except ValueError:
                    try:
                        check_encoding = base64.b64decode(args['enrolement_no'].encode("UTF-8"))
                        valid_enrolement_no = check_encoding.decode("UTF-8")           ## check valid base64
                        if valid_enrolement_no:
                            candidate = Candidate.query.filter_by(enrolement_no=valid_enrolement_no).first()
                            if not candidate:
                                return make_response("No candidate found", 404)
                    except:
                        return make_response("Invalid Input", 401)

        def post(self):
            '''create new candidate'''
            try:
                token = request.headers.get('Authorization')
                
                if token:
                    user_id = User.decode_token(token)
                    if type(user_id) == str:
                        return user_id
                    
                    if not isinstance(user_id, str):
                        parser = reqparse.RequestParser()
                        parser.add_argument('name', required=True)
                        parser.add_argument('address', required=True)
                        parser.add_argument('degree_name', required=True)
                        
                        args = parser.parse_args()

                        new_candidate = Candidate(enrolement_no=str(uuid.uuid4()), name=args['name'],
                        address=args['address'], degree_name=args['degree_name'],
                        admission_status=False)

                        new_candidate.save()
                        response = jsonify({
                            'enrolement_no': new_candidate.enrolement_no,
                            'name': new_candidate.name,
                            'address': new_candidate.address,
                            'degree_name': new_candidate.degree_name,
                            'admission_status': new_candidate.admission_status
                        })
                        return make_response(response, 201)
            except Exception as err:
                return ("Error: ", err)


        def get(self):
            ''' To get a candidate '''
            try:
                token = request.headers.get('Authorization')
                parser = reqparse.RequestParser()
                parser.add_argument('enrolement_no')
                args = parser.parse_args()
                if not args.get('enrolement_no'):
                    return make_response("Please provide enrolement number to update", 404)
                
                if token:
                    user_id = User.decode_token(token)
                    
                    if type(user_id) == str:
                        return user_id

                    if not isinstance(user_id, str):
                        
                        candidate_data = {}
                        
                        encoded_enrolement_no = base64.b64encode(candidate.enrolement_no.encode("UTF-8"))
                        encoded_name = base64.b64encode(candidate.name.encode("UTF-8"))
                        encoded_address = base64.b64encode(candidate.address.encode("UTF-8"))
                        encoded_admission_status = base64.b64encode(str(candidate.admission_status).encode("UTF-8"))
                        encoded_degree_name = base64.b64encode(candidate.degree_name.encode("UTF-8"))
                        
                        candidate_data['enrolement_no'] = encoded_enrolement_no.decode("UTF-8")
                        candidate_data['name'] = encoded_name.decode("UTF-8")
                        candidate_data['address'] = encoded_address.decode("UTF-8")
                        candidate_data['admission_status'] = encoded_admission_status.decode("UTF-8")
                        candidate_data['degree_name'] = encoded_degree_name.decode("UTF-8")

                    return make_response({'candidate':candidate_data}, 200)
                else:
                    return make_response("Access Denied", 403)
            except Exception as err:
                    return {'Error': err}


        def put(self):
            '''To update the candidate'''
            try:
                token = request.headers.get('Authorization')
                parser = reqparse.RequestParser()
                parser.add_argument('enrolement_no')
                args = parser.parse_args()

                if not args.get('enrolement_no'):
                    return make_response("Please provide enrolement number to update", 404)

                if token:
                    user_id = User.decode_token(token)
                    if type(user_id) == str:
                        return user_id
                    if not isinstance(user_id, str):
                        parser = reqparse.RequestParser()
                        
                        parser.add_argument('name', required=True)
                        parser.add_argument('address', required=True)
                        parser.add_argument('admission_status')
                        parser.add_argument('degree_name', required=True)

                        args2 = parser.parse_args()

                        candidate.name = args2['name']
                        candidate.address = args2['address']
                        candidate.admission_status = args2['admission_status']
                        candidate.degree_name = args2['degree_name']
                        candidate.save()

                        return make_response('Candidate has been updated successfully', 200)
                else:
                    return make_response("Access Denied", 403)
            except Exception as err:
                return {'Error': err}


        def delete(self):
            '''To delete the candidate'''
            try:
                token = request.headers.get('Authorization')
                if token:
                    user_id = User.decode_token(token)
                    if type(user_id) == str:
                        return user_id
                    if not isinstance(user_id, str):
                        candidate.delete()
                        return make_response("Candidate has been deleted successfully", 200)
                else:
                    return make_response("Access Denied", 403)
            except Exception as err:
                return {'Error': err}


class Candidate_list(MethodView):
    def get(self):
        try:
            token = request.headers.get('Authorization')
            if token:
                user_id = User.decode_token(token)
                if type(user_id) == str:
                    return user_id
                if not isinstance(user_id, str):
                    candidates = Candidate.query.all()
                
                    if not candidates:
                        return ('No candidate found')

                    output = []
                    for candidate in candidates:
                        candidate_data = {}
                        
                        encoded_enrolement_no = base64.b64encode(candidate.enrolement_no.encode("UTF-8"))
                        encoded_name = base64.b64encode(candidate.name.encode("UTF-8"))
                        encoded_address = base64.b64encode(candidate.address.encode("UTF-8"))
                        encoded_admission_status = base64.b64encode(str(candidate.admission_status).encode("UTF-8"))
                        encoded_degree_name = base64.b64encode(candidate.degree_name.encode("UTF-8"))

                        candidate_data['enrolement_no'] = encoded_enrolement_no.decode("UTF-8")
                        candidate_data['name'] = encoded_name.decode("UTF-8")
                        candidate_data['address'] = encoded_address.decode("UTF-8")
                        candidate_data['admission_status'] = encoded_admission_status.decode("UTF-8")
                        candidate_data['degree_name'] = encoded_degree_name.decode("UTF-8")
                        output.append(candidate_data)
                    return make_response({'candidate': output}, 200)
            else:
                return make_response("Access Denied", 403)
        except Exception as err:
            return {'Error': err}

