import os, sys

def check_login(username, password):
	if username == "test@test.com" and password == "foobar":
		return 1, 1001
	return 0, 0

def get_user_details(uid):
	if uid == 1001:
		return{'display_name': "Foobar!", 'account_created': None}
	return None

def create_pending_user(userEmail, userDisplayName, userPassCrypt, claimOsmName):
	return 1002, 0, "4h4d85w7385jf7d63hsj"

def notify_new_user(userEmail, userDisplayName, claimOsmName, emailToken):
	return None

