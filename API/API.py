from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import abort
import json
import requests

server_rooms='127.0.0.1:5400'
server_canteen='127.0.0.1:5300'
server_secretariats='127.0.0.1:5200'

app = Flask(__name__)

# room location endpoint
@app.route('/location/<id>')
def room_location(id):
	
	r = requests.get('http://'+server_rooms+'/location/'+id)
	if r.status_code!=200:
		abort(r.status_code)
	json_r = r.json()
	return jsonify(json_r)

# room timetable endpoint
@app.route('/timetable/<id>')
def room_timetable(id):
	
	r = requests.get('http://'+server_rooms+'/timetable/'+id)
	if r.status_code!=200:
		abort(r.status_code)
	json_r = r.json()
	return jsonify(json_r)

# canteen menu endpoint
@app.route('/menus')
def canteen_menus():
	
	r = requests.get('http://'+server_canteen+'/menus')
	if r.status_code!=200:
		abort(r.status_code)
	json_r = r.json()
	return jsonify(json_r)

# secretariat listall endpoint
@app.route('/secretariats')	
def list_secretariats():

	r = requests.get('http://'+server_secretariats+'/listAll')
	if r.status_code!=200:
		abort(r.status_code)
	json_r = r.json()
	return jsonify(json_r)

# get secretariat endpoint
@app.route('/secretariats/<id>')	
def get_secretariat(id):
	
	r = requests.get('http://'+server_secretariats+'/getSecretariat/'+id)
	if r.status_code!=200:
		abort(r.status_code)
	json_r = r.json()
	return jsonify(json_r)


if __name__ == '__main__':

    app.run(port=5100, debug=True)
