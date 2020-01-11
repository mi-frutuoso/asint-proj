from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import abort
from flask_cors import CORS
import json
import requests

server_rooms='127.0.0.1:5400'
server_canteen='127.0.0.1:5300'
server_secretariats='127.0.0.1:5200'

import time

# define log file
api_file='logAPI.txt'

app = Flask(__name__)
CORS(app)

# function to register log access
def write_log(filename, logtype, params):
    timestamp=time.strftime("%b %d %Y %H:%M:%S")
    f = open(filename, "a+")
    f.write("[%s] %s - %s\n" %(logtype, timestamp, params))
    f.close()

# room location endpoint
@app.route('/rooms/<id>')
def room_location(id):
	try:
		r = requests.get('http://'+server_rooms+'/rooms/'+id)
		if r.status_code!=200:
			abort(r.status_code)
		json_r = r.json()
		write_log(api_file, 'ROOMS', 'get -- id:'+id+' (code:'+str(r.status_code)+')')
		return jsonify(json_r)
	except requests.exceptions.RequestException:
		abort(500)

# canteen menu endpoint
@app.route('/menus')
def canteen_menus():
	try:
		r = requests.get('http://'+server_canteen+'/menus')
		if r.status_code!=200:
			abort(r.status_code)
		json_r = r.json()
		write_log(api_file, 'CANTEEN', 'menus (code:'+str(r.status_code)+')')
		return jsonify(json_r)
	except requests.exceptions.RequestException:
		abort(500)

# secretariat listall endpoint
@app.route('/secretariats')	
def list_secretariats():
	try:
		r = requests.get('http://'+server_secretariats+'/listAll')
		if r.status_code!=200:
			abort(r.status_code)
		json_r = r.json()
		write_log(api_file, 'SECRETARIATS', 'list (code:'+str(r.status_code)+')')
		return jsonify(json_r)
	except requests.exceptions.RequestException:
		abort(500)

# get secretariat endpoint
@app.route('/secretariats/<id>')	
def get_secretariat(id):
	
	try:
		r = requests.get('http://'+server_secretariats+'/getSecretariat/'+id)
		if r.status_code!=200:
			abort(r.status_code)
		json_r = r.json()
		write_log(api_file, 'SECRETARIATS', 'get - id:'+id+' (code:'+str(r.status_code)+')')
		return jsonify(json_r)
	except requests.exceptions.RequestException:
		abort(500)


if __name__ == '__main__':

    app.run(port=5100, debug=True, host='0.0.0.0')
