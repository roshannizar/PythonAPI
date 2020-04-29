from firebase_admin import auth
from flask import jsonify


# sign in method
def signIn(data, db):
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
