from flask_restful import Resource, Api
from flask_api import FlaskAPI
from flask.views import MethodView
from . import candidate_blueprint
from .views import crud_candidateView, Candidate_list
# Define the API resource
candidate_view = crud_candidateView.as_view('candidate_view')
candidate_list_view = Candidate_list.as_view('candidate_list_view')
candidate_blueprint.add_url_rule('/candidate', view_func=candidate_view, methods=['GET', 'POST', 'PUT', 'DELETE'])
candidate_blueprint.add_url_rule('/candidate_list', view_func=candidate_list_view, methods=['GET'])