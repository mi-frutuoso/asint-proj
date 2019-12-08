from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import json
import requests


app = Flask(__name__)

# main index
@app.route('/location/<id>')
def room_location(id):
	
	r = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+id)
	json_r=r.json()
	campus_r = json_r['topLevelSpace']['name']
	
	r = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+json_r['parentSpace']['id'])
	json_r=r.json()
	building_r = json_r['parentSpace']['name']

	return jsonify(campus=campus_r,building=building_r)

# main index
@app.route('/timetable/<id>')
def room_timetable(id):
	
	r = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+id)
	json_r=r.json()
	events_r = json_r['events']
	

	return jsonify(events=events_r)

if __name__ == '__main__':

    app.run(port=5200, debug=True)
