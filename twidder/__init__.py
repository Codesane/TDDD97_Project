# TDDD97 Lab 2
# 
# Laborants: felno295, perek586

from database_helper import DatabaseHelper
from flask import Flask, jsonify, request, Response
import flask, binascii, os, json
from geventwebsocket import WebSocketApplication
import threading

app = Flask(__name__)

app.secret_key = "46515d0b26a3f598a05f01a5b4108843"

db_helper = DatabaseHelper()

sessions = {}
session_lock = threading.Lock()

__get_session = lambda key: None if key not in sessions else sessions[key]

def get_session(key):
	session_lock.acquire()
	sess = __get_session(key)
	session_lock.release()
	return (key, sess) if sess != None else None

def remove_session(key):
	session_lock.acquire()

	sess = __get_session(key)

	exists = sess != None

	if exists:
		sessions.pop(key)

	session_lock.release()

	return (key, sess) if exists else None
	
	
# Websocket configs

websockets = {}

class WebsocketAppli(WebSocketApplication):
	def on_open(self):
		pass
		# self.ws.send('Welcome, Client.')

	def on_message(self, message):
		if(message and message[:len('register:')] == 'register:'):
			self.token = message[len('register:'):]

			websockets[self.token] = self
			print('Registered new active session: ' + self.token)
		

	def on_close(self, reason):
		print('WSConnection closed.')
		if self.token:
			websockets.pop(self.token, None)




@app.route('/', methods = ['GET'])
def index():
	return app.send_static_file('index.html')

@app.route('/<path:path>', methods = ['GET'])
def assets(path):
	return app.send_static_file(path)


@app.route('/api/sign_in', methods = ['POST'])
def sign_in():

	json = request.get_json(force = True)

	user = db_helper.get_user_by_credentials(json['email'], json['password'])

	gen_token = binascii.hexlify(os.urandom(16))

	if not user:
		return not_found()
	else:
		user_id = user[0]

		session_lock.acquire()

		for k in sessions:
			if sessions[k] == user_id:
				if k in websockets:
					print('k found in websockets, kicking.')
					websockets[k].ws.send('exit')
				sessions.pop(k)
				break

		sessions[gen_token] = user_id
		session_lock.release()

		response_data = {
			'success': True,
			'data': {
				'token': gen_token,
				'email': user[1]
			}
		}

		response = jsonify(response_data)

		response.set_cookie('token', value = gen_token)

		return response


@app.route('/api/sign_up', methods = ['POST'])
def sign_up():

	required = ['email', 'password', 'firstname', 'familyname', 'gender', 'city', 'country']

	json = request.get_json(force = True)

	email = json['email']
	password = json['password']
	first_name = json['firstname']
	family_name = json['familyname']
	gender = json['gender']
	city = json['city']
	country = json['country']

	user_id = db_helper.register_user(email, password, first_name, family_name, gender, city, country)

	response = jsonify({
		'success': True,
		'message': 'Successfully registered.'
	})

	response.status_code = 200

	return response


@app.route('/api/sign_out', methods = ['GET'])
def sign_out():

	token = ''

	for k in request.cookies:
		print(request.cookies[k])

	if 'token' in request.cookies:
		token = request.cookies['token']
	else:
		return bad_request()

	session_lock.acquire()
	success = sessions.pop(token, -1) > -1
	session_lock.release()

	message = 'Successfully logged out.'

	if not success:
		message = 'Invalid Token.'

	json = {
		'success': success,
		'message': message
	}

	response = jsonify(json)
	response.set_cookie('token', '', expires = 0)

	return response

@app.route('/api/change_password', methods = ['PUT'])
def change_password():
	json = request.get_json(force = True)

	token = ''

	if 'token' in request.cookies:
		token = request.cookies['token']
	else:
		return bad_request()

	old_password = json['old_password']
	new_password = json['new_password']

	sess = get_session(token)

	user_id = sess[1] if sess != None else None

	if not user_id:
		invalid_token_response = {
			'success': False,
			'message': 'Invalid Token.'
		}
		return jsonify(invalid_token_response)


	if not db_helper.check_password_match(user_id, old_password):
		incorrect_password = {
			'success': False,
			'message': 'Your current password does not match the supplied one.'
		}
		return jsonify(incorrect_password)

	db_helper.user_change_password(user_id, new_password)

	response = {
		'success': True,
		'message': 'Your password has been changed.'
	}

	return jsonify(response)


@app.route('/api/user', methods = ['GET'])
def get_user_data_by_token():
	token = ''

	if 'token' in request.cookies:
		token = request.cookies['token']
	else:
		return bad_request()


	sess = get_session(token)

	u_id = sess[1] if sess != None else None

	if not u_id:
		return not_found()

	user = db_helper.get_user_by_id(u_id)

	if not user:
		return not_found()

	response = {
		'success': True,
		'data': {
			'id': user[0],
			'firstname': user[1],
			'familyname': user[2],
			'gender': user[3],
			'country': user[4],
			'email': user[5],
			'city': user[6]
		}
	}

	return jsonify(response)


@app.route('/api/user/<string:email>', methods = ['GET'])
def get_user_data_by_email(email):
	token = ''

	if 'token' in request.cookies:
		token = request.cookies['token']
	else:
		return bad_request()

	sess = get_session(token)
	u_id = sess[1] if sess != None else None

	if not u_id:
		return forbidden()

	if not db_helper.user_exists(u_id):
		return not_found()

	user = db_helper.get_user_by_email(email)

	if not user:
		return not_found()

	response = {
		'success': True,
		'data': {
			'id': user[0],
			'firstname': user[1],
			'familyname': user[2],
			'gender': user[3],
			'country': user[4],
			'email': user[5],
			'city': user[6]
		}
	}

	return jsonify(response)


"""
	Just a helper function
"""
def posts_to_json(posts):
	json_response = []
	for post in posts:

		json_post = {
			'id' : post[0],
			'message': post[1],
			'poster_email': post[2]
		}

		# Append the fetched message to the array.
		json_response.append(json_post)

	return Response(json.dumps(json_response), mimetype = 'application/json')


@app.route('/api/posts', methods = ['GET'])
def get_user_posts_by_token():
	token = ''

	if 'token' in request.cookies:
		token = request.cookies['token']
	else:
		return bad_request()

	sess = get_session(token)
	u_id = sess[1] if sess != None else None

	if not u_id:
		return forbidden()

	messages = db_helper.get_user_posts_by_id(u_id)

	return posts_to_json(messages)

@app.route('/api/posts/<string:email>', methods = ['GET'])
def get_user_posts_by_email(email):
	token = ''

	if 'token' in request.cookies:
		token = request.cookies['token']
	else:
		return bad_request()

	sess = get_session(token)
	u_id = sess[1] if sess != None else None

	if not u_id:
		return forbidden()

	if not db_helper.get_user_by_id(u_id):
		return forbidden()

	user_messages = db_helper.get_user_posts_by_email(email)

	return posts_to_json(user_messages)


@app.route('/api/post', methods = ['POST'])
def post_message_to_self():
	json = request.get_json(force = True)
	token = ''

	if 'token' in request.cookies:
		token = request.cookies['token']
	else:
		return bad_request()

	message = json['message']

	sess = get_session(token)
	u_id = sess[1] if sess != None else None

	if not u_id:
		return forbidden()

	db_helper.post_message_to_id(u_id, u_id, message)

	response = {
		'success': True,
		'message': 'Your message was posted.'
	}

	return jsonify(response)


@app.route('/api/post/<string:email>', methods = ['POST'])
def post_message(email):
	json = request.get_json(force = True)
	token = ''

	if 'token' in request.cookies:
		token = request.cookies['token']
	else:
		return bad_request()

	message = json['message']

	sess = get_session(token)
	u_id = sess[1] if sess != None else None

	if not u_id:
		return forbidden()

	db_helper.post_message_to_email(u_id, email, message)

	response = {
		'success': True,
		'message': 'Your message was posted.'
	}

	return jsonify(response)

@app.errorhandler(403)
def forbidden(error = None):
	json = {
		'success': False,
		'message': 'You do not have access to this information.'
	}
	response = jsonify(json)
	response.status_code = 403

	return response

@app.errorhandler(400)
def bad_request(error = None):
	json = {
		'success': False,
		'message': 'Bad Request'
	}

	response = jsonify(json)
	response.status_code = 400

	return response

@app.errorhandler(404)
def not_found(error = None):
	json = {
		'success': False,
		'message': 'Not found'
	}

	response = jsonify(json)
	response.status_code = 404

	return response















