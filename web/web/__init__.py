from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	config = Configurator(settings=settings)
	config.include('pyramid_chameleon')

	my_session_factory = SignedCookieSessionFactory(settings['auth.secret'])
	config.set_session_factory(my_session_factory)

	config.include('pyramid_mailer')

	config.add_static_view('static', 'static', cache_max_age=60)
	config.add_route('home', '/')
	config.add_route('register', '/register')
	config.add_route('login', '/login')
	config.add_route('logout', '/logout')
	config.add_route('confirmuser', '/confirmuser')
	config.scan()
	return config.make_wsgi_app()

