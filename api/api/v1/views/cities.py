#!/usr/bin/python3
"""
Handles all the default RESTFul API actions for the app
"""


from api.v1.views import app_views
from models.city import City
from models.state import State
from flask import abort, jsonify, request
from models import storage

@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False)
def state_cities_id(state_id):
    """
    Returns the list of cities of State with id state_id
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    all_cities = []
    for city in cities:
        all_cities.append(city.to_dict())
    return jsonify(all_cities)

@app_views.route("/cities/<city_id>", strict_slashes=False)
def city_id(city_id):
    """
    Returns the City with id state_id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city = city.to_dict()
    return jsonify(city)

@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city_id(city_id):
    """
    Delete the City with id city_id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def post_city(state_id):
    """
    Create a new city for a state
    """
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return jsonify({"message": "Not a JSON"}), 400
    content = request.get_json()
    if "name" not in content:
        return jsonify({"message": "Missing name"}), 400
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city = City()
    for key, value in content.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.state_id = state.id
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201

@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
def put_city_id(city_id):
    """
    Put the State with id state_id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return jsonify({"message": "Not a JSON"}), 400
    content = request.get_json()
    for key, value in content.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
