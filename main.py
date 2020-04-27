import flask
import firebase_admin
import google

from firebase_admin import credentials, firestore, auth

# flask initialization
from flask import request, jsonify, json

app = flask.Flask(__name__)

# registering certificate
cred = credentials.Certificate("serviceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()


# signup API
@app.route('/v1/signup', methods=['POST'])
def login():
    number = auth.create_user(email='roshannizar@gmail.com',
                              email_verified=False,
                              phone_number='+94771914959',
                              password='123456',
                              display_name='Roshan Nizar',
                              photo_url='http://www.example.com/12345678/photo.png',
                              disabled=False)
    print(number)


# add data to  collection
@app.route('/v1/create', methods=['POST'])
def create():
    data = request.form
    print(data)
    # doc_ref = db.collection('testing').add({
    #     'reply': 'Here we go!'
    # })
    # print(doc_ref)


# update data
@app.route('/v1/update', methods=['PUT'])
def update():
    db.collection('testing').document("GUJfBrmLDq4ul2WzwReg").update({
        'reply': 'Vola'
    })


# delete data
@app.route('/v1/delete', methods=["DELETE"])
def delete():
    db.collection('testing').document("RFMkEQkAoFWsTTz350YR").delete()


# get data
@app.route('/data', methods=['GET'])
def getData():
    try:
        docs = db.collection('testing').stream()
        listDocs = []
        for doc in docs:
            listDocs.append(doc.to_dict())
        response = jsonify(listDocs)
        response.status_code = 200
        return response
    except google.cloud.exceptions.NotFound:
        response = jsonify(listDocs)
        response.status_code = 500
        return response


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)