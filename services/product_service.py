from flask import jsonify


def getProducts(db):
    docs = db.collection('products').stream()
    listDocs = []
    for doc in docs:
        listDocs.append(doc.to_dict())
    response = jsonify(listDocs)
    response.status_code = 200
    return response
