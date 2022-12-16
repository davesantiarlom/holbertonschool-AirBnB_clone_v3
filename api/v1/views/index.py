#!/usr/bin/python3
""" This script handles returning JSON format of
    certain variables """
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/api/v1/status')
def return_status():
    """ Returns the status code OK in JSON format """
    return {"status": "OK"}


@app_views.route('/api/v1/stats', strict_slashes=False)
def status():
    classes = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(classes)
