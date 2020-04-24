import firebase_admin
import google
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()


# add data to  collection
doc_ref = db.collection('testing').add({
    'reply': 'Santa'
})

# update data
db.collection('testing').document("GUJfBrmLDq4ul2WzwReg").update({
    'reply': 'Vola'
})

# delete data
db.collection('testing').document("RFMkEQkAoFWsTTz350YR").delete()

# get data
try:
    docs = db.collection('testing').stream()
    for doc in docs:
        print(format(doc.to_dict()))

except google.cloud.exceptions.NotFound:
    print('No Doc Found!')
