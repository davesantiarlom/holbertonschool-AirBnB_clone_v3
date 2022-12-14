#!/usr/bin/python3
""" This script starts a Flask web application.
    Handles cities and states using RESTful API """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/api/v1/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def getstatecity(state_id):
    """returns cities of a state"""
    state_list = storage.get('State', state_id)
    if state_list is None:
        abort(404)
    city_list = []
    for obj in state_list.cities:
        city_list.append(obj.to_dict())
    return jsonify(city_list)


@app_views.route('/api/v1/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def postcity(state_id):
    """posts city to a state"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    jsoned = request.get_json()
    if jsoned is None:
        abort(400, 'Not a JSON')
    if 'name' not in jsoned:
        abort(400, 'Missing name')
    new_city = City(state_id=state_id, **jsoned)
    storage.new(new_city)
    storage.save()
    #  new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/api/v1/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def getcity(city_id):
    """get's city's id"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/api/v1/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletecity(city_id):
    """deletes city"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def putcity(city_id):
    """updates city"""
    jsoned = request.get_json()
    if jsoned is None:
        abort(400, 'Not a JSON')
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    for key, value in jsoned.items():
        if key in ['id', 'created_at', 'updated_at', 'state_id']:
            continue
        setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
