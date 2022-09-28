"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/register', methods=['POST'])
def register():
    body = request.get_json()
    # tengo que comprobar si esxise un usuario con mismo correo en la base de datos
    one_people = User.query.filter_by(email=body['email']).first()
    if one_people:
        return jsonify({"error": "ya existe"}),418
    else:
        crear_user = User(email=body['email'], password=body['password'], is_active=True)
        db.session.add(crear_user)
        db.session.commit()

        return jsonify(body),201

@api.route('/login', methods=['POST'])
def login():
    body= request.get_json()
    # tengo que comprobar si esxise un usuario con mismo correo en la base de datos
    one_people = User.query.filter_by(email=body['email'], password=body['password']).first()
    if one_people:
        token= create_access_token(identity='email')
        return jsonify({"access_token": token, "mensaje": "inicio de sesion correcto"}), 200
    else:
        return jsonify({"error": "no existe usuario registrado con esos datos"}),418

@api.route('/privada', methods=['GET'])
@jwt_required()
def privada():
    identidad= get_jwt_identity()
    return jsonify({"mensaje": "tienes permiso para entrar", "permiso": True, "email":identidad})