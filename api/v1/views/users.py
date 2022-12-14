#!/usr/bin/python3
""" This script starts a Flask web application.
    Handles amenities using RESTful API """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/api/v1/users', methods=['GET'],
                 strict_slashes=False)
def getallusers():
    """Get all users"""
    user_list = []
    for obj in storage.all('User').values():
        user_list.append(obj.to_dict())
    return jsonify(user_list)


@app_views.route('/api/v1/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def getuserid(user_id):
    """Get users by id"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/api/v1/users', methods=['POST'],
                 strict_slashes=False)
def postusers():
    """posts users"""
    jsoned = request.get_json()
    if jsoned is None:
        abort(400, 'Not a JSON')
    if 'email' not in jsoned:
        abort(400, 'Missing email')
    if 'password' not in jsoned:
        abort(400, 'Missing password')
    new_u = User(**jsoned)
    new_u.save()
    return jsonify(new_u.to_dict()), 201


@app_views.route('/api/v1/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteuser(user_id):
    """deletes user"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def putuser(user_id):
    """updates user"""
    jsoned = request.get_json()
    if jsoned is None:
        return 'Not a JSON', 400
    user_list = storage.get('User', user_id)
    if user_list is None:
        abort(404)
    for key, value in jsoned.items():
        if key in ['id', 'created_at', 'updated_at', 'state_id']:
            continue
        setattr(user_list, key, value)
    storage.save()
    return jsonify(user_list.to_dict()), 200
