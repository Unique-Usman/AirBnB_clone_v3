#!/usr/bin/python3
"""
Handles all the default RESTFul API actions for city
"""


from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from flask import abort, jsonify, request
from models import storage

@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False)
def city_places_id(city_id):
    """
    Returns the list of place of City with id city_id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = city.places
    all_places = []
    for place in places:
        all_places.append(place.to_dict())
    return jsonify(all_places)

@app_views.route("/places/<place_id>", strict_slashes=False)
def place_id(place_id):
    """
    Returns the Place with id place_id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place = place.to_dict()
    return jsonify(place)

@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place_id(place_id):
    """
    Delete the Place with id place_id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """
    Create a new place for a City
    """
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return jsonify({"message": "Not a JSON"}), 400
    content = request.get_json()
    if "name" not in content:
        return jsonify({"message": "Missing name"}), 400
    if "user_id" not in content:
        return jsonify({"message": "Missing user_id"}), 400
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    user_id = content["user_id"]
    user = storage.get(User, user_id)
    if not user_id:
        abort(404)
    place = Place()
    for key, value in content.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    place.place_id = city.id
    place.user_id = user.id
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201

@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def put_place_id(place_id):
    """
    Put the Place with id place_id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return jsonify({"message": "Not a JSON"}), 400
    content = request.get_json()
    for key, value in content.items():
        if key not in ["id", "created_at", "updated_at", "city_id", "user_id"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
