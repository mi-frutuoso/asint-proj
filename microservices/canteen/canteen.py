from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import json
import requests


app = Flask(__name__)

# canteen menus endpoint
@app.route('/menus')
def canteen_menus():
	
	r = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen?day=26/1/2019')
	if r.status_code!=200:
		abort(404)
	json_r=r.json()

	return jsonify(json_r)

if __name__ == '__main__':

    app.run(port=5300, debug=True)
