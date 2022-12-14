#!/usr/bin/python3
""" This script starts a Flask web application """
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def end_session(self):
    """ Terminate the session to generate a new one """
    storage.close()


@app.errorhandler(404)
def error_404(self):
    """ Error 404. Handles this particular error message """
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST')
    if host is None:
        host = '0.0.0.0'
    port = getenv('HBNB_API_PORT')
    if port is None:
        port = 5000

    app.run(host=host, port=port, threaded=True)
