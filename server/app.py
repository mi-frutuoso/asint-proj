from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import abort
import json
# include custom files
import sys
import requests
sys.path.insert(0, 'src') #include folder src
# from src.utils import User

from flask_login import LoginManager
from flask import session, redirect, url_for, escape

app = Flask(__name__)

app.secret_key = b'\x1a2\xc5\xe81\x12\xc3\x80JPp\xbe\xa1\x9a\xe1,'


@app.route('/')
def hello():
    return '<h2>Welcome to backend server.</h2>'

@app.route('/admin')
def index():
    if 'username' in session:
        return render_template('admin.html', user=escape(session['username']))
    return render_template('admin_logout.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('admin_login.html')

@app.route('/admin/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


# add secretariat front-end
@app.route('/frontend/addSecretariat')
def index_add(result=None):
    if 'username' in session:
        return render_template('add.html', result=result)
    return render_template('admin_logout.html')


# add secretariat -- route that processes the input from the frontend form (add.html)
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
    print(r.status_code)
    print(r.json()) #debug -- print response from API
    if(r.status_code == 200):
        return "Success. <a href='/frontend/listSecretariats'>Go to secretariats page</a>"
    return "An error occured (%d). <a href='/frontend/listSecretariats'>Go to secretariats page</a>" % (r.status_code)


@app.route('/frontend/listSecretariats', methods=['GET'])
def get_secretariats():
    if 'username' in session:
        r = requests.get('http://localhost:5200/listAll')
        if r.status_code!=200:
            abort(404)
        listSecretariats = r.json()
        return render_template('secretariats.html', items=listSecretariats)
    return render_template('admin_logout.html')
    
# edit secretariat front-end
@app.route('/frontendEditSecretariat/<id>') #get, post
def index_edit(id):
    if 'username' in session:
        s = get_secretariat(id)
        return render_template("edit.html", 
            location=s['location'], name=s['name'], description=s['description'], opening_hours=s['opening_hours'], id=id)
    return render_template('admin_logout.html')

def get_secretariat(id):
    r = requests.get('http://localhost:5200/getSecretariat/'+id)
    if r.status_code!=200:
       abort(404)
    return r.json()

# handle form edit information
@app.route('/editSecretariat/<id>', methods=['POST'])
def send_edit(id):
    sID = id
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
    r = requests.post('http://localhost:5200/editSecretariat/'+sID, json=obj) # forward form data to API of microservice Secretariats
    print(r.json()) #debug -- print response from API
    if(r.status_code == 200):
        return "Success. <a href='/frontend/listSecretariats'>Return to the previous page</a>"
    return "An error occured (%d). <a href='/frontend/listSecretariats'>Return to the previous page</a>" % (r.status_code)


if __name__ == '__main__':

    app.run(port=5500, debug=True)
