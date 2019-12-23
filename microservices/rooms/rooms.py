from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import abort
import json
import requests


app = Flask(__name__)

# room location endpoint
@app.route('/rooms/<id>')
def room_location(id):
	
	#Request room information
	r = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+id)
	if r.status_code!=200:
		abort(404)
	json_r=r.json()
	if 'topLevelSpace' and 'parentSpace' not in json_r:
		abort(500)
	name_r = json_r['name']
	campus_r = json_r['topLevelSpace']['name']
	events_r = json_r['events']

	#Request floor information
	try:
		r = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+json_r['parentSpace']['id'])
		if r.status_code!=200:
			abort(404)
		json_r=r.json()
		if 'parentSpace' not in json_r:
			abort(500)
		building_r = json_r['parentSpace']['name']
	except requests.exceptions.RequestException:
		abort(500)
	#Return json
	return jsonify(name=name_r, campus=campus_r, building=building_r, events=events_r)

if __name__ == '__main__':

    app.run(port=5400, debug=True)
