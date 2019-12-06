from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import json
# include custom files
import sys
import requests
sys.path.insert(0, 'src') #include folder src
from src.utils import Storage

app = Flask(__name__)
st = Storage()


# main index
@app.route('/')
def hello_world():
    s = st.getSize()
    ks = st.getKeys()
    return render_template("index.html", counter = s, keys = ks)

# add secretariat front-end
@app.route('/frontend/addSecretariat') #get, post
def index(result=None):
    if request.args.get('location', None):
        result = process_text(request.args['location'])
    return render_template('form2.html', result=result)

def process_text(text):
    return "FOO" + text

# add specific secretariat TEST
@app.route('/test/apiaddSpecificSecretariat')
def send_spost():
    json_send = {
        'location':'civil',
        'name':'secretaria de civil',
        'description':'descri',
        'opening_hours':'2a-6a 9h-16h'
    }
    print(json_send) #debug
    r = requests.post('http://localhost:5200/addSecretariat', json=json_send)
    print(r.json())
    return sent_spost(json.dumps(json_send), r.text) #render_template('movies.html', movies=json.loads(r.text)['movies'])

def sent_spost(sent, recv):
    return "<p>sent: "+sent+"</p><p>received: "+recv+"</p>"

# add secretariat -- route that processes the input from the frontend form (form2.html)
@app.route('/api/addSecretariat', methods=['POST'])
def send_post():
    location = request.form["location"]
    name = request.form["name"]
    description = request.form["description"]
    opening_hours = request.form["opening_hours"]
    obj = {
        'location':location,
        'name':name,
        'description':description,
        'opening_hours':opening_hours
    }
    print(obj) #debug
    r = requests.post('http://localhost:5200/addSecretariat', json=obj) # forward form data to API of microservice Secretariats
    print(r.json()) #debug -- print response from API
    return sent_post(json.dumps(obj), r.text) #render_template('movies.html', movies=json.loads(r.text)['movies'])

def sent_post(sent, recv):
    return "<p>sent: "+sent+"</p><p>received: "+recv+"</p>"

# @app.route('/some-url')
# def get_data():
#     return requests.get('http://example.com').content

# read secretariat
@app.route('/frontend/secretariats/<key>')
def get_Value(key):
    val = st.getValue(key)
    if val == None:
        return render_template("notFound.html", error_id=key)
    return str(val) # default

if __name__ == '__main__':

    app.run(port=5000, debug=True)

    # user_json = json.loads(request.get_json())
    # first_name = user_json.get('first_name')
    # last_name = user_json.get('last_name')
    # email = user_json.get('email')