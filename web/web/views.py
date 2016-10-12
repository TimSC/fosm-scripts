from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'web'}

@view_config(route_name='login', renderer='templates/login.pt')
def login_view(request):
    return {'project': 'web'}

