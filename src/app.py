"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Nationality, Stand, Character, Favorite
#from models import Person

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({"msg": "Missing data"}), 400
    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return jsonify({"msg": "User already exists"}), 400
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user.serialize()), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify(user.serialize()), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted"}), 200

@app.route('/nationalities', methods=['POST'])
def create_nationality():
    data = request.get_json()
    if not data or not data.get('country'):
        return jsonify({"msg": "Missing data"}), 400
    if Nationality.query.filter_by(country=data['country']).first():
        return jsonify({"msg": "Nationality already exists"}), 400
    nat = Nationality(country=data['country'], description=data.get('description'))
    db.session.add(nat)
    db.session.commit()
    return jsonify(nat.serialize()), 201

@app.route('/nationalities', methods=['GET'])
def get_nationalities():
    nats = Nationality.query.all()
    return jsonify([n.serialize() for n in nats]), 200

@app.route('/nationalities/<int:nat_id>', methods=['GET'])
def get_nationality(nat_id):
    nat = Nationality.query.get(nat_id)
    if not nat:
        return jsonify({"msg": "Nationality not found"}), 404
    return jsonify(nat.serialize()), 200

@app.route('/nationalities/<int:nat_id>', methods=['PUT'])
def update_nationality(nat_id):
    nat = Nationality.query.get(nat_id)
    if not nat:
        return jsonify({"msg": "Nationality not found"}), 404
    data = request.get_json()
    nat.country = data.get('country', nat.country)
    nat.description = data.get('description', nat.description)
    db.session.commit()
    return jsonify(nat.serialize()), 200

@app.route('/nationalities/<int:nat_id>', methods=['DELETE'])
def delete_nationality(nat_id):
    nat = Nationality.query.get(nat_id)
    if not nat:
        return jsonify({"msg": "Nationality not found"}), 404
    db.session.delete(nat)
    db.session.commit()
    return jsonify({"msg": "Nationality deleted"}), 200

@app.route('/characters', methods=['POST'])
def create_character():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('nationality_id'):
        return jsonify({"msg": "Missing data"}), 400
    if Character.query.filter_by(name=data['name']).first():
        return jsonify({"msg": "Character already exists"}), 400
    character = Character(
        name=data['name'],
        age=data.get('age'),
        nationality_id=data['nationality_id']
    )
    db.session.add(character)
    db.session.commit()
    return jsonify(character.serialize()), 201

@app.route('/characters', methods=['GET'])
def get_characters():
    chars = Character.query.all()
    return jsonify([c.serialize() for c in chars]), 200

@app.route('/characters/<int:char_id>', methods=['GET'])
def get_character(char_id):
    char = Character.query.get(char_id)
    if not char:
        return jsonify({"msg": "Character not found"}), 404
    return jsonify(char.serialize()), 200

@app.route('/characters/<int:char_id>', methods=['PUT'])
def update_character(char_id):
    char = Character.query.get(char_id)
    if not char:
        return jsonify({"msg": "Character not found"}), 404
    data = request.get_json()
    char.name = data.get('name', char.name)
    char.age = data.get('age', char.age)
    char.nationality_id = data.get('nationality_id', char.nationality_id)
    db.session.commit()
    return jsonify(char.serialize()), 200

@app.route('/characters/<int:char_id>', methods=['DELETE'])
def delete_character(char_id):
    char = Character.query.get(char_id)
    if not char:
        return jsonify({"msg": "Character not found"}), 404
    db.session.delete(char)
    db.session.commit()
    return jsonify({"msg": "Character deleted"}), 200

@app.route('/stands', methods=['POST'])
def create_stand():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('character_id'):
        return jsonify({"msg": "Missing data"}), 400
    if Stand.query.filter_by(name=data['name']).first():
        return jsonify({"msg": "Stand already exists"}), 400
    if Stand.query.filter_by(character_id=data['character_id']).first():
        return jsonify({"msg": "This character already has a Stand"}), 400
    stand = Stand(
        name=data['name'],
        ability=data.get('ability'),
        character_id=data['character_id']
    )
    db.session.add(stand)
    db.session.commit()
    return jsonify(stand.serialize()), 201

@app.route('/stands', methods=['GET'])
def get_stands():
    stands = Stand.query.all()
    return jsonify([s.serialize() for s in stands]), 200

@app.route('/stands/<int:stand_id>', methods=['GET'])
def get_stand(stand_id):
    stand = Stand.query.get(stand_id)
    if not stand:
        return jsonify({"msg": "Stand not found"}), 404
    return jsonify(stand.serialize()), 200

@app.route('/stands/<int:stand_id>', methods=['PUT'])
def update_stand(stand_id):
    stand = Stand.query.get(stand_id)
    if not stand:
        return jsonify({"msg": "Stand not found"}), 404
    data = request.get_json()
    stand.name = data.get('name', stand.name)
    stand.ability = data.get('ability', stand.ability)
    stand.character_id = data.get('character_id', stand.character_id)
    db.session.commit()
    return jsonify(stand.serialize()), 200

@app.route('/stands/<int:stand_id>', methods=['DELETE'])
def delete_stand(stand_id):
    stand = Stand.query.get(stand_id)
    if not stand:
        return jsonify({"msg": "Stand not found"}), 404
    db.session.delete(stand)
    db.session.commit()
    return jsonify({"msg": "Stand deleted"}), 200

@app.route('/favorites', methods=['POST'])
def create_favorite():
    data = request.get_json()
    if not data or not data.get('user_id') or (not data.get('character_id') and not data.get('nationality_id')):
        return jsonify({"msg": "Missing data"}), 400
    fav = Favorite(
        user_id=data['user_id'],
        character_id=data.get('character_id'),
        nationality_id=data.get('nationality_id')
    )
    db.session.add(fav)
    db.session.commit()
    return jsonify(fav.serialize()), 201

@app.route('/favorites', methods=['GET'])
def get_favorites():
    favs = Favorite.query.all()
    return jsonify([f.serialize() for f in favs]), 200

@app.route('/favorites/<int:fav_id>', methods=['GET'])
def get_favorite(fav_id):
    fav = Favorite.query.get(fav_id)
    if not fav:
        return jsonify({"msg": "Favorite not found"}), 404
    return jsonify(fav.serialize()), 200

@app.route('/favorites/<int:fav_id>', methods=['PUT'])
def update_favorite(fav_id):
    fav = Favorite.query.get(fav_id)
    if not fav:
        return jsonify({"msg": "Favorite not found"}), 404
    data = request.get_json()
    fav.user_id = data.get('user_id', fav.user_id)
    fav.character_id = data.get('character_id', fav.character_id)
    fav.nationality_id = data.get('nationality_id', fav.nationality_id)
    db.session.commit()
    return jsonify(fav.serialize()), 200

@app.route('/favorites/<int:fav_id>', methods=['DELETE'])
def delete_favorite(fav_id):
    fav = Favorite.query.get(fav_id)
    if not fav:
        return jsonify({"msg": "Favorite not found"}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200
