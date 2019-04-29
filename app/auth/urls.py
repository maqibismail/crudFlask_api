from flask.views import MethodView
from . import auth_blueprint
from .views import RegistrationView, LoginView
#Register and login api's
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')
auth_blueprint.add_url_rule('/auth/register', view_func=registration_view, methods=['POST'])
auth_blueprint.add_url_rule('/auth/login', view_func=login_view, methods=['POST'])