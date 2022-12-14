#!/usr/bin/python3
""" This script starts a Flask web application.
    Handles amenities using RESTful API """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/api/v1/amenities', methods=['GET'],
                 strict_slashes=False)
def getallamenit():
    """Get all amenities"""
    amenit_list = []
    for obj in storage.all('Amenity').values():
        amenit_list.append(obj.to_dict())
    return jsonify(amenit_list)


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def getamenitid(amenity_id):
    """Get amenities by id"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/api/v1/amenities', methods=['POST'],
                 strict_slashes=False)
def postamenity():
    """posts city to a state"""
    jsoned = request.get_json()
    if jsoned is None:
        abort(400, 'Not a JSON')
    name = jsoned.get('name')
    if name is None:
        abort(400, 'Missing name')
    new_a = Amenity(**jsoned)
    new_a.save()
    return jsonify(new_a.to_dict()), 201


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteamenit(amenity_id):
    """deletes amenity"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def putamenit(amenity_id):
    """updates amenity"""
    jsoned = request.get_json()
    if jsoned is None:
        abort(400, 'Not a JSON')
    amenit_list = storage.get('Amenity', amenity_id)
    if amenit_list is None:
        abort(404)
    for key, value in jsoned.items():
        if key in ['id', 'created_at', 'updated_at', 'state_id']:
            continue
        setattr(amenit_list, key, value)
    storage.save()
    return jsonify(amenit_list.to_dict()), 200
