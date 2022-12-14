#!/usr/bin/python3
""" This script starts a Flask web application.
    Handles reviews using RESTful API"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/api/v1/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """ Retrieves and displays all reviews by given
        place_id, if possible """
    place_list = storage.get('Place', place_id)
    if place_list is None:
        abort(404)
    review_list = []
    for obj in place_list.reviews:
        review_list.append(obj.to_dict())

    return jsonify(review_list)


@app_views.route('/api/v1/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_specific_review(review_id):
    """ Retrieves and displays the Review object by given
        review_id, if possible """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/api/v1/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Retrieves and deletes the Review object by given
        state_id, if possible """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a new Review object and associates it with
        the given place_id, if possible """
    json_list = request.get_json()
    if json_list is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in json_list:
        abort(400, 'Missing user_id')
    if 'text' not in json_list:
        abort(400, 'Missing text')
    if storage.get('Place', place_id) is None:
        abort(404)
    if storage.get('User', json_list['user_id']) is None:
        abort(404)

    new_review = Review(place_id=place_id, **json_list)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/api/v1/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Retrieves and updates the Review object by the given
        review_id, if possible """
    update_me = request.get_json()
    if update_me is None:
        abort(400, 'Not a JSON')
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    for key, value in update_me.items():
        if key not in ['id', 'created_at', 'updated_at',
                       'user_id', 'place_id']:
            setattr(review, key, value)

    storage.save()
    return review.to_dict(), 200
