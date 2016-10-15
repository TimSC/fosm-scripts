import os, sys
from gtm import GTM
from cStringIO import StringIO

#Unescaping approach http://stackoverflow.com/a/12614706/4288232
import HTMLParser as html

#Get the call in table file
if 'gtm_access_ci' not in os.environ:
	print "Please set environment variable gtm_access_ci to the location of gtm_access.ci"
	exit(0)
if not os.path.exists(os.environ['gtm_access_ci']):
	print "Error: {0} does not exist".format(os.environ['gtm_access_ci'])
	exit(0)
os.environ['GTMCI'] = os.environ['gtm_access_ci']

#Change working folder to database location
if 'gtm_data_dir' not in os.environ:
	print "Please set environment variable gtm_data_dir to the data folder"
if not os.path.exists(os.environ['gtm_data_dir']):
	print "Error: {0} does not exist".format(os.environ['gtm_data_dir'])
	exit(0)

originalDir = os.getcwd()
os.chdir(os.environ['gtm_data_dir'])
db = GTM()
os.chdir(originalDir)

def check_login(username, password):
	global db
	os.chdir(os.environ['gtm_data_dir'])
	
	db.execute(b'd loginLowLevel^user("{0}","{1}")'.format(username.encode('ascii', 'xmlcharrefreplace'), 
		password.encode('ascii', 'xmlcharrefreplace')))
	result = int(db.get('%sess("authenticated")')), int(db.get('%sess("uid")'))

	os.chdir(originalDir)
	return result

def get_user_details(uid):
	global db
	os.chdir(os.environ['gtm_data_dir'])

	h = html.HTMLParser()
	display_name = h.unescape(db.get('^user({0},"name")'.format(int(uid))))
	account_created = h.unescape(db.get('^user({0},"createdAt")'.format(int(uid))))
	
	os.chdir(originalDir)
	return {'display_name': display_name, 'account_created': account_created}

