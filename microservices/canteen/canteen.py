from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import abort
import json
import requests


app = Flask(__name__)

# canteen menus endpoint
@app.route('/menus')
def canteen_menus():
	try:
		r = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen')
		if r.status_code!=200:
			abort(404)
		json_r=r.json()
		return jsonify(json_r)
	except requests.exceptions.RequestException:
		abort(500)

if __name__ == '__main__':

    app.run(port=5300, debug=True)
