from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import json
import requests


app = Flask(__name__)

# main index
@app.route('/menus')
def canteen_menus():
	
	r = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen')
	json_r=r.json()

	return jsonify(json_r)

if __name__ == '__main__':

    app.run(port=5300, debug=True)
