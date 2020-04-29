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


# sign in API
@app.route('/v1/signin', methods=['POST'])
def signIn():
    try:
        data = request.form
        user = auth.get_user_by_phone_number(data['phone_number'])

        profile_data = db.collection('profile').document(user.uid).get()

        password = profile_data.to_dict()

        if password['password'] == data['password']:
            response = jsonify(user.uid)
            response.status_code = 200
            return response
        else:
            response = jsonify('{Invalid Credentials}')
            response.status_code = 404
            return response

    except google.cloud.exceptions.NotFound:
        response = jsonify('{Invalid credentials, Please try again}')
        response.status_code = 404
        return response
    except google.cloud.exceptions.InternalServerError:
        response = jsonify('{Popped out an error, please contact the administrator}')
        response.status_code = 500
        return response


# signup API
@app.route('/v1/signup', methods=['POST'])
def signUp():
    data = request.form
    try:
        number = auth.create_user(phone_number=data['phone_number']).uid

        db.collection('profile').document(number).set({
            'firstName': data['first_name'],
            'lastName': data['last_name'],
            'email': data['email'],
            'phoneNumber': data['phone_number'],
            'password': data['password'],
            'uid': number,
            'profile_url': data['profile_url']
        })

        response = jsonify('{Account created successfully}')
        response.status_code = 200
        return response

    except google.cloud.exceptions.NotFound:
        response = jsonify('{Bad Request}')
        response.status_code = 404
        return response
    except google.cloud.exceptions.InternalServerError:
        response = jsonify('{Error occurred while signing you up}')
        response.status_code = 500
        return response


# add data to  collection
@app.route('/v1/create', methods=['POST'])
def create():
    data = request.form
    print(data['name'])
    return data['name']
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
        response = jsonify('{no values}')
        response.status_code = 500
        return response


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
