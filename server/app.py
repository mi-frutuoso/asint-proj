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

import time

# define log files
backend_file='logBackend.txt'
api_file='logAPI.txt'
auth_file='logAuth.txt'

#api 
server_secretariats='127.0.0.1:5200'

app = Flask(__name__)

app.secret_key = b'\x1a2\xc5\xe81\x12\xc3\x80JPp\xbe\xa1\x9a\xe1,'

# function to register log access
def write_log(filename, logtype, params):
    timestamp=time.strftime("%b %d %Y %H:%M:%S")
    f = open(filename, "a+")
    f.write("[%s] %s - %s\n" %(logtype, timestamp, params))
    f.close()


@app.route('/')
def hello():
    return render_template('index.html')

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
            write_log(backend_file, 'BACKEND:web', 'login:'+session['username'])
            return redirect(url_for('index'))
        return render_template('admin_login.html', trigger="yes")
    return render_template('admin_login.html')

@app.route('/admin/logout')
def logout():
    # remove the username from the session if it's there
    write_log(backend_file, 'BACKEND:web', 'logout:'+session['username'])
    session.pop('username', None)
    return redirect(url_for('index'))


# add secretariat front-end
@app.route('/frontend/addSecretariat')
def index_add(result=None):
    if 'username' in session:
        write_log(backend_file, 'BACKEND:web', 'admin - addSecretariat')
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
    r = requests.post('http://'+server_secretariats+'/addSecretariat', json=obj) # forward form data to API of microservice Secretariats
    print(r.status_code) # debug
    json_response=r.json()
    print(r.json()) #debug -- print response from API
    write_log(backend_file, 'SECRETARIAT', 'admin - add - info:'+str(obj)+' - id:'+json_response['answer']+' (code:'+str(r.status_code)+')')
    if(r.status_code == 200):
        msg = "Success. %d" %(r.status_code)
    else:
        msg = "Error. %d" % (r.status_code)
    return render_template('result.html', msg=msg, header="ADD")

# request all existing secretariats
@app.route('/frontend/listSecretariats', methods=['GET'])
def get_secretariats():
    if 'username' in session:
        r = requests.get('http://'+server_secretariats+'/listAll')
        if r.status_code!=200:
            abort(404)
        listSecretariats = r.json()
        write_log(backend_file, 'SECRETARIAT', 'admin - list'+' (code:'+str(r.status_code)+')')
        return render_template('secretariats.html', items=listSecretariats)
    return render_template('admin_logout.html')
    
# edit secretariat front-end
@app.route('/frontendEditSecretariat/<id>') #get, post
def index_edit(id):
    if 'username' in session:
        s = get_secretariat(id)
        write_log(backend_file, 'BACKEND:web', 'admin - editSecretariat')
        return render_template("edit.html", 
            location=s['location'], name=s['name'], description=s['description'], opening_hours=s['opening_hours'], id=id)
    return render_template('admin_logout.html')

def get_secretariat(id):
    r = requests.get('http://'+server_secretariats+'/getSecretariat/'+id)
    write_log(backend_file, 'SECRETARIAT', 'admin - get - id:'+id+' (code:'+str(r.status_code)+')')
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
    r = requests.post('http://'+server_secretariats+'/editSecretariat/'+sID, json=obj) # forward form data to API of microservice Secretariats
    print(r.json()) #debug -- print response from API
    write_log(backend_file, 'SECRETARIAT', 'admin - edit - id:'+sID+' - newInfo:'+str(obj)+' (code:'+str(r.status_code)+')')
    if(r.status_code == 200):
        msg = "Success. %d" %(r.status_code)
    else:
        msg = "Error. %d" % (r.status_code)
    return render_template('result.html', msg=msg, header="EDIT")

# handle delete request
@app.route('/deleteSecretariat/<id>')
def send_delete(id):
    r = requests.get('http://'+server_secretariats+'/deleteSecretariat/'+id) # forward delete request to API of microservice Secretariats
    print(r.json()) #debug -- print response from API
    write_log(backend_file, 'SECRETARIAT', 'admin - delete - id:'+id+' (code:'+str(r.status_code)+')')
    if(r.status_code == 200):
        return "ok"
    return "not ok"

# show log files
@app.route('/frontend/logs')
def show_logs():
    if 'username' in session:
        back_list = []
        api_list = []
        auth_list = []
        try:
            f = open(backend_file, "r")
            for line in f:
                back_list.append(line)
        except IOError:
            print('%s not found' %backend_file)
            back_list = ''
        finally:
            f.close()
        
        try:
            f = open('../API/'+api_file, "r")
            for line in f:
                api_list.append(line)
        except IOError:
            print('%s not found' %api_file)
            api_list = ''
        finally:
            f.close()

        try:    
            f = open(auth_file, "r") # TODO: change dir file
            for line in f:
                auth_list.append(line)
        except IOError:
            print('%s not found' %auth_file)
            auth_list = ''
        finally:
            f.close()

        return render_template('logs.html', back=back_list, api=api_list, auth=auth_list)
    return render_template('admin_logout.html')

if __name__ == '__main__':

    app.run(port=5500, debug=True)
