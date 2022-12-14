#!/usr/bin/python3
""" This script starts a Flask web application.
    Handles places using RESTful API """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/api/v1/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """ Retrieves and displays all Place objects by given
        city_id, if possible """
    city_list = storage.get('City', city_id)
    if city_list is None:
        abort(404)
    place_list = []
    for obj in city_list.places:
        place_list.append(obj.to_dict())

    return jsonify(place_list)


@app_views.route('/api/v1/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_specific_place(place_id):
    """ Retrieves and displays the Place object by given
        place_id, if possible """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/api/v1/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Retrieves and deletes the Place object by given
        place_id, if possible """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a new Place object and associate it with
        the given city_id, if possible """
    json_list = request.get_json()
    if json_list is None:
        abort(400, 'Not a JSON')
    if 'name' not in json_list:
        abort(400, 'Missing name')
    if 'user_id' not in json_list:
        abort(400, 'Missing user_id')
    if storage.get('City', city_id) is None:
        abort(404)
    if storage.get('User', json_list['user_id']) is None:
        abort(404)

    new_place = Place(city_id=city_id, **json_list)
    storage.new(new_place)
    storage.save()
    # new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/api/v1/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ Retrieves and updates the Place object by the given
        place_id, if possible """
    update_me = request.get_json()
    if update_me is None:
        abort(400, 'Not a JSON')
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    for key, value in update_me.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(place, key, value)

    storage.save()
    return place.to_dict(), 200
