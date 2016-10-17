import os, sys
from gtm import GTM
from xml.sax.saxutils import escape

#Unescaping approach http://stackoverflow.com/a/12614706/4288232
import HTMLParser as html

def Enc(val):
	val = escape(val)
	return val.replace("=", "&#61;")

class GtmWrapper(object):
	def __init__(self):
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

		self.originalDir = os.getcwd()
		os.chdir(os.environ['gtm_data_dir'])
		self.db = GTM()
		os.chdir(self.originalDir)

	def __del__(self):
		del self.db
		os.chdir(self.originalDir)	

	def check_login(self, username, password):
		global db
		os.chdir(os.environ['gtm_data_dir'])
	
		self.db.execute(b'd loginLowLevel^user("{0}","{1}")'.format(Enc(username), Enc(password)))
		result = int(self.db.get('%sess("authenticated")')), int(self.db.get('%sess("uid")'))

		os.chdir(self.originalDir)
		return result

	def get_user_details(self, uid):
		global db
		os.chdir(os.environ['gtm_data_dir'])

		h = html.HTMLParser()
		display_name = h.unescape(self.db.get('^user({0},"name")'.format(int(uid))))
		account_created = h.unescape(self.db.get('^user({0},"createdAt")'.format(int(uid))))
	
		os.chdir(self.originalDir)
		return {'display_name': display_name, 'account_created': account_created}

	def create_pending_user(self, userEmail, userDisplayName, userPassCrypt, claimOsmName):
		global db
		os.chdir(os.environ['gtm_data_dir'])

		postData = []
		postData.append(b"userEmail={0}".format(Enc(userEmail)))
		postData.append(b"userEmailConfirmation={0}".format(Enc(userEmail)))
		postData.append(b"userDisplayName={0}".format(Enc(userDisplayName)))
		postData.append(b"userPassCrypt={0}".format(Enc(userPassCrypt)))
		postData.append(b"userPassCryptConfirmation={0}".format(Enc(userPassCrypt)))
		postData.append(b"claimOsmName={0}".format('on' if claimOsmName else 'off'))
		postStr = "&".join(postData)
	
		self.db.set(b'%ENV("POST_DATA")', postStr)

		self.db.execute(b'd createInsertIntoDb^user')
	
		uid = self.db.get('%sess("uid")')
		numErrors = int(self.db.get('errors'))
		errors = []
		for i in range(1, numErrors+1):
			errors.append((self.db.get('errors("1","field")'), self.db.get('errors("1","message")')))
		emailToken = self.db.get('%sess("emailToken")')

		os.chdir(self.originalDir)
		return uid, errors, emailToken

	def notify_new_user(self, userEmail, userDisplayName, claimOsmName, emailToken):
		global db
		os.chdir(os.environ['gtm_data_dir'])

		postData = []
		postData.append(b"userEmail={0}".format(Enc(userEmail)))
		postData.append(b"userDisplayName={0}".format(Enc(userDisplayName)))
		postData.append(b"claimOsmName={0}".format(Enc(claimOsmName)))
		postStr = "&".join(postData)
	
		self.db.set(b'%ENV("POST_DATA")', postStr)

		self.db.execute(b'd createInformByEmail^user("{0}")'.format(emailToken))

		os.chdir(self.originalDir)
		return None

	def get_pending_uid_from_token(self, token):
		global db
		os.chdir(os.environ['gtm_data_dir'])

		self.db.execute(b'd getUidFromToken^user("{0}")'.format(Enc(token)))
		if not int(self.db.get('exists')):
			raise RuntimeError("User not found")
		uid = int(self.db.get('uid'))

		os.chdir(self.originalDir)
		return uid

	def confirm_user(self, pendingUid):
		global db
		os.chdir(os.environ['gtm_data_dir'])

		self.db.execute(b'd lowLevelApprove^user("{0}")'.format(int(pendingUid)))

		uid = int(self.db.get('uid')) #Get final uid

		os.chdir(self.originalDir)	
		return uid

