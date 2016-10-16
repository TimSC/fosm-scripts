from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import gtm_wrapper
#import nulldb_wrapper

db_wrapper = gtm_wrapper.GtmWrapper()

@view_config(route_name='home', renderer='templates/index.pt')
def home_view(request):

	username = None
	if "username" in request.session:
		username = request.session["username"]

	return {'logged_in': username}

@view_config(route_name='register', renderer='templates/register.pt')
def register_view(request):

	userEmail = request.params.get('userEmail')
	userEmailConfirmation = request.params.get('userEmailConfirmation', '')
	userDisplayName = request.params.get('userDisplayName', '')
	userPassCrypt = request.params.get('userPassCrypt', '')
	userPassCryptConfirmation = request.params.get('userPassCryptConfirmation', '')
	claimOsmName = request.params.get('claimOsmName', 'off') == 'on'
	messageOccured = False
	messageContent = None
	registerSuccess = False

	errors = 0
	if 'form.submitted' in request.params:
		if userEmail != userEmailConfirmation:
			errors += 1
		if userPassCrypt != userPassCryptConfirmation:
			errors += 1
		if len(userPassCrypt) < 6:
			errors += 1
		if len(userDisplayName) < 3:
			errors += 1

		if errors == 0:
			uid, errors, emailToken = db_wrapper.create_pending_user(userEmail, userDisplayName, userPassCrypt, claimOsmName)

		if errors == 0:
			messageOccured=True
			messageContent="Thank you. Please check your email."
			registerSuccess=True

	username = None
	if "username" in request.session:
		username = request.session["username"]

	return {'logged_in': username,
		'messageOccured': messageOccured,
		'messageContent': messageContent,
		'errorOccured': errors > 0,
		'userEmail': userEmail,
		'userEmailConfirmation': userEmailConfirmation,
		'userDisplayName': userDisplayName,
		'userPassCrypt': userPassCrypt,
		'userPassCryptConfirmation': userPassCryptConfirmation,
		'claimOsmName': claimOsmName,
		'registerSuccess': registerSuccess,
		}

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

@view_config(route_name='confirmuser')
def confirm_user_view(request):

	token = request.params.get('token')
	#db_wrapper.confirm_user(token)

	url = request.route_url('home')
	return HTTPFound(location=url)

