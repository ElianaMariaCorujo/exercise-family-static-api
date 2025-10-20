import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure 

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

# 1. Endpoint: [GET] /members (Obtener todos)
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# 2. Endpoint: [GET] /members/<int:member_id> (Obtener uno)
@app.route('/members/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    member = jackson_family.get_member(member_id)
    
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"message": "Member not found"}), 404

# 3. Endpoint: [POST] /members (Añadir uno)
# --- ¡ESTA ES LA CORRECCIÓN! ---
@app.route('/members', methods=['POST'])
def add_new_member():
    body = request.get_json(silent=True)

    if body is None:
        return jsonify({"message": "Bad request: JSON body is missing"}), 400
    
    # 1. Validación SIN el 'id' (porque el test no lo envía)
    required_fields = ['first_name', 'age', 'lucky_numbers']
    if not all(field in body for field in required_fields):
        return jsonify({"message": "Bad request: Missing required fields"}), 400

    # 2. Creamos el miembro nuevo aquí
    new_member = {
        "id": jackson_family._generateId(), # <-- Generamos el ID
        "first_name": body["first_name"],
        "age": body["age"],
        "lucky_numbers": body["lucky_numbers"],
        "last_name": jackson_family.last_name
    }

    # 3. Lo añadimos a la familia
    jackson_family.add_member(new_member)
    
    # 4. Devolvemos el miembro NUEVO (no un mensaje)
    #    (Esto es lo que el test necesita para el KeyError)
    return jsonify(new_member), 200

# 4. Endpoint: [DELETE] /members/<int:member_id> (Eliminar uno)
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_one_member(member_id):
    success = jackson_family.delete_member(member_id)
    
    if success:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"message": "Member not found"}), 404

# --- Boilerplate ---
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)