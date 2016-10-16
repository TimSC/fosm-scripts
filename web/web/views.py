from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import gtm_wrapper as db_wrapper
#import nulldb_wrapper as db_wrapper

@view_config(route_name='home', renderer='templates/index.pt')
def my_view(request):

	username = None
	if "username" in request.session:
		username = request.session["username"]

	return {'project': 'web', 'logged_in': username}

@view_config(route_name='login', renderer='templates/login.pt')
def login_view(request):
	login = ""
	password = ""
	message = None
	login_url = request.route_url('login')
	referrer = request.url
	if referrer == login_url:
		referrer = '/'  # never use login form itself as came_from
	came_from = request.params.get('came_from', referrer)

	if 'form.submitted' in request.params:
		login = request.params['login']
		password = request.params['password']
		ok, uid = db_wrapper.check_login(login, password)
		if ok:
			userDetails = db_wrapper.get_user_details(uid)
			request.session["username"] = userDetails["display_name"]
			request.session["account_created"] = userDetails["account_created"]
			return HTTPFound(location=came_from)
		message = 'Failed login'

	return {'url': request.application_url + '/login',
			'login': login,
			'password': password,
			'came_from': came_from,
			'message': message,
		}

@view_config(route_name='logout')
def logout_view(request):

	request.session.invalidate()
	url = request.route_url('home')
	return HTTPFound(location=url)

