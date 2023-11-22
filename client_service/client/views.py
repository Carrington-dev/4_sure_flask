from flask import request, jsonify
from .models import Client, ClientSchema

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)

@app.route("/clients", methods=["GET"])
def get_clients():
    clients = Client.query.all()
    result = clients_schema.dump(clients)
    return jsonify(result.data)

@app.route("/clients", methods=["POST"])
def add_client():
    # Check if user is authenticated
    client = Client(user_id=g.user.id, **request.json)
    if not check_authentication(client.id):
        return jsonify({'error': 'Unauthorized'}), 401

    db.session.add(client)
    db.session.commit()
    return client_schema.jsonify(client)

@app.route("/clients/<id>", methods=["GET"])
def get_client(id):
    client = Client.query.get(id)
    return client_schema.jsonify(client)

@app.route("/clients/<id>", methods=["PUT"])
def update_client(id):
    # Check if user is authenticated
    client = Client.query.get(id)
    if not check_authentication(client.id):
        return jsonify({'error': 'Unauthorized'}), 401
    client.contact_name = request.json['contact_name']
    client.contact_email = request.json['contact_email']
    client.contact_number = request.json['contact_number']
    db.session.commit()
    return client_schema.jsonify(client)