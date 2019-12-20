from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import json

# include custom files
import sys
sys.path.insert(0, 'src') #include folder src
from src.utils import Storage


app = Flask(__name__)
st = Storage()

# main index
@app.route('/')
def hello_world():
    return render_template("index.html")

# add secretariat - API
@app.route('/addSecretariat', methods=['POST'])
def add_secretariat():
    if(request.is_json):
        rcvd_json = request.get_json(force=True)
        # parse rcvd_json:
        location = rcvd_json["location"]
        name = rcvd_json["name"]
        description = rcvd_json["description"]
        opening_hours = rcvd_json["opening_hours"]

        id=st.store(location, name, description, opening_hours)
        ret = {'answer':id}
        jsonify(ret)
        return ret # returns an answer (client is expecting a json, but the protocol can be changed)
    else:
        return "XXXX" #pass


# read secretariat
@app.route('/getSecretariat/<key>')
def get_secretariat(key):
    s = st.getSecretariat(key) # key = ID
    if s == None:
        return "get secretariat error or inexisting"
    return s


# list secretariat locations
@app.route('/listAll', methods=['GET'])
def get_allSec():
    list_ = st.listAll()
    if list_ == None:
        return "list all secretariats error or empty"
    return jsonify(list_)

# edit secretariat
@app.route('/editSecretariat/<id>', methods=['POST'])
def edit_secretariat(id):
    if(request.is_json):
        rcvd_json = request.get_json(force=True)
        answer = st.edit(id, rcvd_json)
        ret = {'answer':answer}
        jsonify(ret)
        return ret
    else:
        return "XXXX" #pass

# delete secretariat
@app.route('/deleteSecretariat/<id>', methods=['GET'])
def delete_secretariat(id):
    st.delete(id)
    #ret = {'answer':answer}
    #jsonify(ret)
    return "ok"

if __name__ == '__main__':

    app.run(port=5200, debug=True)