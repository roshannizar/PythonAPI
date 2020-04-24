import flask
import firebase_admin
import google

from firebase_admin import credentials, firestore

# flask initialization
app = flask.Flask(__name__)

# registering certificate
cred = credentials.Certificate("serviceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()


# add data to  collection
@app.route('/v1/create', methods=['POST'])
def create():
    doc_ref = db.collection('testing').add({
        'reply': 'Here we go!'
    })
    print(doc_ref)


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
@app.route('/', methods=['GET'])
def getData():
    try:
        docs = db.collection('testing').stream()
        for doc in docs:
            print(format(doc.to_dict()))

    except google.cloud.exceptions.NotFound:
        print('No Doc Found!')


app.run()
