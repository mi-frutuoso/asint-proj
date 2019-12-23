from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import abort
from flask import redirect
from flask import send_file

import json
import requests
from users import User
import time


import string
import random
import threading

redirect_uri = "http://127.0.0.1:5000/userAuth" # this is the address of the page on this app

uri_api = "http://127.0.0.1:5100"


client_id= "1695915081465951" # copy value from the app registration
clientSecret = "dV8OqovYTvGa/xJhh5G5+Ciyz40LlG2f8KEk7hfRexhjKsJvT5xqbwdAbO+aRn5/wZ26mRal+gg5KaS4iZeBWg==" # copy value from the app registration


fenixLoginpage= "https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=%s&redirect_uri=%s"
fenixacesstokenpage = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'

log_file='logAuth.txt'


app = Flask(__name__)

user_list = []

# room location endpoint
@app.route('/')
def main_menu():

	if 'key' in request.args:

		key = request.args['key']

		for user in user_list:
			if user.key==key:
				params = {'access_token': user.access_token}
				resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
				if resp.status_code==200:
					r_json = resp.json()
					return render_template("main_menu.html", username=r_json['name'], key=key, photo_data = r_json['photo']['data'], photo_type=r_json['photo']['type'])

	redPage = fenixLoginpage % (client_id, redirect_uri)
	return redirect(redPage)

@app.route('/userAuth')
def userAuthenticated():
	code = request.args['code']
	payload = {'client_id': client_id, 'client_secret': clientSecret, 'redirect_uri' : redirect_uri, 'code' : code, 'grant_type': 'authorization_code'}
	response = requests.post(fenixacesstokenpage, params = payload)

	if response.status_code==200:
		r_json = response.json()
		user = User(r_json['access_token'])
		user_list.append(user)
		return redirect('/?key='+user.key)

	abort(401)

@app.route('/qrReader')
def qr_reader():

	name, key, photo_data, photo_type = Authentication()

	return render_template("qr_reader.html", username=name, key=key, photo_data = photo_data, photo_type=photo_type, api=uri_api)

@app.route('/canteen')
def canteen():

	name, key, photo_data, photo_type = Authentication()

	resp = requests.get(uri_api+"/menus")
	if resp.status_code==200:
		r_json = resp.json()

	return render_template("canteen.html", username=name, key=key, photo_data = photo_data, photo_type=photo_type, menus=r_json)

@app.route('/validation')
def validate():

	name, key, photo_data, photo_type = Authentication()

	return render_template("validation.html", username=name, key=key, photo_data = photo_data, photo_type=photo_type)

@app.route('/qr-scanner.min.js')
def file1_send():
	return send_file("qr_scanner/qr-scanner.min.js")	

@app.route('/qr-scanner-worker.min.js')
def file2_send():	
	return send_file("qr_scanner/qr-scanner-worker.min.js")

# request secret
@app.route('/validation/request')
def val_request():

	name, key, photo_data, photo_type = Authentication()
	# generate secret until it is unique
	flag_continue=0
	while True:
		secret = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(7))
		for user in user_list:
			if user.secret==secret:
				flag_continue=1
				break
		if(flag_continue):
			continue
		else:
			break
	
	for user in user_list:
		if user.key==key:
			user.secret=secret
			user.event=threading.Event()
			break
	# "wait" for some user to request the secret
	return render_template("request.html", username=name, key=key, photo_data = photo_data, photo_type=photo_type, secret=secret)

# validate secret
@app.route('/validation/wait')
def val_wait():

	name, key, photo_data, photo_type = Authentication()

	for user in user_list:
		if user.key==key:
			user.event.wait()

			params = {'access_token': user.visitor_token}
			resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
			if resp.status_code==200:
				r_json = resp.json()
			else:
				abort(500)
			
			user.visitor_token = None
			user.event = None

			break

	ret_html = """
		<p><b>"""+r_json['name']+"""</b> has just used your secret.</p>
		<div class="col-xs-3">
			<img src="data:"""+r_json['photo']['type']+"""+;base64,"""+r_json['photo']['data']+"""" align="right"/>
		</div>
	"""
	
	return ret_html

	
# validate secret
@app.route('/validation/validate', methods=['POST'])
def val_response():
	reqSecret = request.form['secret']
	name, key, photo_data, photo_type = Authentication()
	flag_found=0
	for user in user_list:
		if user.secret==reqSecret:
			flag_found=1
			params = {'access_token': user.access_token}
			resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
			if resp.status_code==200:
				r_json = resp.json()
			else:
				abort(500)
			# clear secret
			user.secret=None
			
			for user2 in user_list:
				if user2.key==key:
					user.visitor_token=user2.access_token
					break

			# now notice the searched user that their secret has been used
			user.event.set()
			break

	write_log(log_file, 'VALIDATION', 'Person1:'+name+' Person2:'+r_json['name'])

	if(flag_found == 0):
		return render_template("validate.html", notFound='yes', secret=reqSecret, username=name, key=key, photo_data = photo_data, photo_type=photo_type)	
	return render_template("validate.html", username=name, key=key, photo_data = photo_data, photo_type=photo_type, secret=reqSecret, reqUser=r_json['name'], reqPhoto=r_json['photo']['data'], reqPhotoType=r_json['photo']['type'])

def Authentication():
	if 'key' in request.args:

		key = request.args['key']

		for user in user_list:
			if user.key==key:
				params = {'access_token': user.access_token}
				resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
				if resp.status_code==200:
					r_json = resp.json()
					return r_json['name'], key, r_json['photo']['data'], r_json['photo']['type']
	abort(401)

# function to register log access
def write_log(filename, logtype, params):
    timestamp=time.strftime("%b %d %Y %H:%M:%S")
    f = open(filename, "a+")
    f.write("[%s] %s - %s\n" %(logtype, timestamp, params))
    f.close()

if __name__ == '__main__':

    app.run(port=5000, debug=True, threaded=True)
