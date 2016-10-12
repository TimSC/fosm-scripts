from pyramid.config import Configurator
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.security import Everyone, Authenticated
from pyramid.authentication import AuthTktCookieHelper
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.settings import asbool

def asint(val):
	if val == 'None':
		return None
	return int(val)

class GtmAuthenticate(object):
	#Based on http://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/auth/custom.html
	
	def __init__(self, settings):
		self.cookie = AuthTktCookieHelper(
			settings.get('auth.secret'),
			cookie_name=settings.get('auth.token') or 'auth_tkt',
			secure=asbool(settings.get('auth.secure')),
			timeout=asint(settings.get('auth.timeout')),
			reissue_time=asint(settings.get('auth.reissue_time')),
			max_age=asint(settings.get('auth.max_age')),
		)

	def remember(self, request, principal, **kw):
		return self.cookie.remember(request, principal, **kw)

	def forget(self, request):
		return self.cookie.forget(request)

	def unauthenticated_userid(self, request):
		result = self.cookie.identify(request)
		if result:
			return result['userid']

	def authenticated_userid(self, request):
		if request.user:
			return request.user.id

	def effective_principals(self, request):
		principals = [Everyone]
		user = request.user
		if user:
			principals += [Authenticated, 'u:%s' % user.id]
			principals.extend(('g:%s' % g.name for g in user.groups))
		return principals


def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	config = Configurator(settings=settings)
	config.include('pyramid_chameleon')

	config.set_authentication_policy(GtmAuthenticate(settings=settings))
	config.set_authorization_policy(ACLAuthorizationPolicy())

	config.add_static_view('static', 'static', cache_max_age=3600)
	config.add_route('home', '/')
	config.add_route('login', '/login')
	config.scan()
	return config.make_wsgi_app()

