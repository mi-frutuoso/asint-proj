from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import abort
from flask import redirect
import json
import requests
from users import User

import string
import random
import threading

redirect_uri = "http://127.0.0.1:5000/userAuth" # this is the address of the page on this app


client_id= "1695915081465951" # copy value from the app registration
clientSecret = "dV8OqovYTvGa/xJhh5G5+Ciyz40LlG2f8KEk7hfRexhjKsJvT5xqbwdAbO+aRn5/wZ26mRal+gg5KaS4iZeBWg==" # copy value from the app registration


fenixLoginpage= "https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=%s&redirect_uri=%s"
fenixacesstokenpage = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'


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

	return render_template("qr_reader.html", username=name, key=key, photo_data = photo_data, photo_type=photo_type)

@app.route('/canteen')
def canteen():

	name, key, photo_data, photo_type = Authentication()

	return render_template("canteen.html", username=name, key=key, photo_data = photo_data, photo_type=photo_type)

@app.route('/validation')
def validate():

	name, key, photo_data, photo_type = Authentication()

	return render_template("validation.html", username=name, key=key, photo_data = photo_data, photo_type=photo_type)	

secret_submitted = threading.Event()
responsible_user = None
responsible_photoData = None
responsible_photoType = None


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
			user.updateSecret(secret)
			break
	# "wait" for some user to request the secret
	return render_template("request.html", username=name, key=key, photo_data = photo_data, photo_type=photo_type, secret=secret)

# validate secret
@app.route('/validation/wait')
def val_wait():
	print("estou à espera")
	# prepare thread
	thread = threading.Thread(target=val_response)
	thread.start()
	secret_submitted.wait()
	global responsible_user
	global responsible_photoData
	global responsible_photoType

	if responsible_user == None:
		print("*********************vou mandar nada")
		return 'yo'

	ret_html = """
		<p><b>"""+responsible_user+"""</b> has just used your secret.</p>
		<div class="col-xs-3">
			<img src="data:"""+responsible_photoType+"""+;base64,"""+responsible_photoData+"""" align="right"/>
		</div>
	"""

	# clear vars
	responsible_user = None
	responsible_photoData = None
	responsible_photoType = None
	
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
				# clear secret
				user.clearSecret()
				global responsible_user
				global responsible_photoData
				global responsible_photoType
				responsible_user = name
				responsible_photoData = photo_data
				responsible_photoType = photo_type
				# now notice the searched user that their secret has been used
				secret_submitted.set()
				break
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



if __name__ == '__main__':

    app.run(port=5000, debug=True)
