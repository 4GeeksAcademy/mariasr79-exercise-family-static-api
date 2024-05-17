"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for # type: ignore
from flask_cors import CORS # type: ignore
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

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

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/members/<int:Id_member>', methods=['GET'])
def handle_get_member(id_member):
    member = jackson_family.get_member(id_member)

    if member is None:
        return jsonify({'err': 'member not found'}), 404
    response = member
    return jsonify(response), 200

@app.route('/member', methods=['POST'])
def add_member():
    member_data = request.json
    if not member_data:
        return jsonify({'error': 'Invalid input'}), 400
    
    jackson_family.add_member(member_data)
    return jsonify({'message': 'Member added successfully'}), 200

@app.route('/member/<int:id_member>', methods=['DELETE'])
def delete_member(id_member):
    member = jackson_family.get_member(id_member)
    if member is None:
        return jsonify({'error': 'Member not found'}), 404
    
    jackson_family.delete_member(id_member)
    return jsonify({'message': 'Member deleted successfully'}), 200

@app.route('/member/<int:id_member>', methods=['PUT'])
def update_member(id_member):
    member_data = request.json
    if not member_data:
        return jsonify({'error': 'Invalid input'}), 400
    
    member = jackson_family.get_member(id_member)
    if member is None:
        return jsonify({'error': 'Member not found'}), 404
    
    jackson_family.update_member(id_member, member_data)
    return jsonify({'message': 'Member updated successfully'}), 200

   
  # this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
