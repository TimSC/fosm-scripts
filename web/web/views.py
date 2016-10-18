from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid_mailer.message import Message
from pyramid_mailer import get_mailer
import gtm_wrapper, os, string, re
#import nulldb_wrapper
import transaction

#Favicons etc
#http://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/static_assets/files.html

db_wrapper = gtm_wrapper.GtmWrapper()

@view_config(route_name='home', renderer='templates/index.pt')
def home_view(request):

	username = None
	if "username" in request.session:
		username = request.session["username"]

	return {'username': username}

def ValidateEmailFormat(addressToVerify):
	match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
	return match is not None

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

	errors = []
	if 'form.submitted' in request.params:
		if userEmail != userEmailConfirmation:
			errors.append(("userEmail", "User email does not match"))
		if userPassCrypt != userPassCryptConfirmation:
			errors.append(("userPassCrypt", "User passwords does not match"))
		if len(userPassCrypt) < 6:
			errors.append(("userPassCrypt", "Password is too short"))
		if len(userDisplayName) < 3:
			errors.append(("userDisplayName", "User name is too short"))
		if len(userDisplayName) > 64:
			errors.append(("userDisplayName", "User name is too long"))
		if not ValidateEmailFormat(userEmail):
			errors.append(("userEmail", "Not a correct email address"))

		if len(errors) == 0:
			uid, errors, emailToken = db_wrapper.create_pending_user(userEmail, userDisplayName, userPassCrypt, claimOsmName)

		if len(errors) == 0:
			here = os.path.abspath(os.path.dirname(__file__))#Is there a better way to find the path?
			senderEmail = request.registry.settings["userconfirm.email_sender"]

			#Email user with link to confirm account
			if len(senderEmail) > 0:
				emailBody = open(os.path.join(here, "templates/confirmemail.txt"), "rt").read()
				emailBody = emailBody.format(name=userDisplayName, emailToken=emailToken, host=request.host)
				message = Message(subject="fosm :: Confirm your account creation request",
		              sender=senderEmail,
		              recipients=[userEmail],
		              body=emailBody)
				mailer = get_mailer(request)
				mailer.send(message)

			adminEmails = map(string.strip, request.registry.settings["userconfirm.admin_emails"].split(","))

			#Inform admin by email of new user
			if len(adminEmails) > 0 and len(senderEmail) > 0:
				emailBody2 = open(os.path.join(here, "templates/informadmin.txt"), "rt").read()
				emailBody2 = emailBody2.format(name=userDisplayName, email=userEmail, claimOsmName=claimOsmName, emailToken=emailToken)
				message2 = Message(subject="fosm signup",
		              sender=senderEmail,
		              recipients=adminEmails,
		              body=emailBody2)
				mailer.send(message2)

			transaction.commit()

			messageOccured=True
			messageContent="Thank you. Please check your email."
			registerSuccess=True

	username = None
	if "username" in request.session:
		username = request.session["username"]

	return {'logged_in': username,
		'messageOccured': messageOccured,
		'messageContent': messageContent,
		'numErrors': len(errors),
		'errorMessages': [tmp[1] for tmp in errors],
		'errorFields': [tmp[0] for tmp in errors],
		'userEmail': userEmail,
		'userEmailConfirmation': userEmailConfirmation,
		'userDisplayName': userDisplayName,
		'userPassCrypt': userPassCrypt,
		'userPassCryptConfirmation': userPassCryptConfirmation,
		'claimOsmName': claimOsmName,
		'registerSuccess': registerSuccess,
		'username': username,
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

	username = None
	if "username" in request.session:
		username = request.session["username"]

	return {'url': request.application_url + '/login',
			'login': login,
			'password': password,
			'came_from': came_from,
			'message': message,
			'username': username,
		}

@view_config(route_name='logout')
def logout_view(request):

	request.session.invalidate()
	url = request.route_url('home')
	return HTTPFound(location=url)

@view_config(route_name='confirmuser', renderer='templates/confirmuser.pt')
def confirm_user_view(request):

	token = request.params.get('token')
	errors = []
	messageOccured = False
	messageContent = None

	try:
		pendingUid = db_wrapper.get_pending_uid_from_token(token)
		db_wrapper.confirm_user(pendingUid)
		messageOccured = True
		messageContent = "Your account has been confirmed. Welcome to FOSM. You can now use JOSM, Merkaartor and other tools to contribute content. "

	except RuntimeError as err:
		errors.append(str(err))	

	username = None
	if "username" in request.session:
		username = request.session["username"]

	return {'logged_in': username,
		'messageOccured': messageOccured,
		'messageContent': messageContent,
		'numErrors': len(errors),
		'errorMessages': errors,
		}

