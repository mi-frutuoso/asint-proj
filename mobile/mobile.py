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

@app.route('/qr-scanner.min.js')
def file1_send():
	return send_file("qr_scanner/qr-scanner.min.js")	

@app.route('/qr-scanner-worker.min.js')
def file2_send():	
	return send_file("qr_scanner/qr-scanner-worker.min.js")


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
