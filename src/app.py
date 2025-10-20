"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
# Importamos la estructura de datos
from datastructures import FamilyStructure 

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# --- INICIO DE NUESTROS ENDPOINTS ---

# 1. Endpoint: [GET] /members (Obtener todos)
@app.route('/members', methods=['GET'])
def get_all_members():

    members = jackson_family.get_all_members()
    
    return jsonify(members), 200

# 2. Endpoint: [GET] /member/<int:member_id> (Obtener uno)
@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
   
    member = jackson_family.get_member(member_id)
    
    if member:
    
        return jsonify(member), 200
    else:
        
        return jsonify({"message": "Member not found"}), 404


@app.route('/member', methods=['POST'])
def add_new_member():
   
    body = request.get_json(silent=True)

   
    if body is None:
        return jsonify({"message": "Bad request: JSON body is missing"}), 400
    
    required_fields = ['id', 'first_name', 'age', 'lucky_numbers']
    if not all(field in body for field in required_fields):
        return jsonify({"message": "Bad request: Missing required fields"}), 400

    jackson_family.add_member(body)

    return jsonify({"message": "Member added"}), 200

# 4. Endpoint: [DELETE] /member/<int:member_id> (Eliminar uno)
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_one_member(member_id):
    success = jackson_family.delete_member(member_id)
    
    if success:
        
        return jsonify({"done": True}), 200
    else:
       
        return jsonify({"message": "Member not found"}), 404

# --- FIN DE NUESTROS ENDPOINTS ---

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
