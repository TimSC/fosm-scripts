from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
import auth

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	config = Configurator(settings=settings)
	config.include('pyramid_chameleon')

	my_session_factory = SignedCookieSessionFactory(settings['auth.secret'])
	config.set_session_factory(my_session_factory)

	config.add_static_view('static', 'static', cache_max_age=60)
	config.add_route('home', '/')
	config.add_route('login', '/login')
	config.add_route('logout', '/logout')
	config.scan()
	return config.make_wsgi_app()

