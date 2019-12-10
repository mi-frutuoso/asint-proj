from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import abort
import json
import requests


app = Flask(__name__)

# room location endpoint
@app.route('/location/<id>')
def room_location(id):
	
	#Request room information
	r = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+id)
	if r.status_code!=200:
		abort(404)
	json_r=r.json()
	if 'topLevelSpace' and 'parentSpace' not in json_r:
		abort(500)
	campus_r = json_r['topLevelSpace']['name']

	#Request floor information
	r = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+json_r['parentSpace']['id'])
	if r.status_code!=200:
		abort(404)
	json_r=r.json()
	if 'parentSpace' not in json_r:
		abort(500)
	building_r = json_r['parentSpace']['name']

	#Return json
	return jsonify(campus=campus_r,building=building_r)

# room timetable endpoint
@app.route('/timetable/<id>')
def room_timetable(id):
	
	#Request room information
	r = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+id)
	if r.status_code!=200:
		abort(404)
	json_r=r.json()
	if 'events' not in json_r:
		abort(500)
	events_r = json_r['events']
	
	#Return json
	return jsonify(events=events_r)

if __name__ == '__main__':

    app.run(port=5400, debug=True)
