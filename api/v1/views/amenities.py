#!/usr/bin/python3
"""
Handles all the default RESTFul API actions for the Amenity Object
"""


from api.v1.views import app_views
from models.amenity import Amenity
from flask import abort, jsonify, request
from models import storage

@app_views.route("/amenities", strict_slashes=False)
def amenities():
    """
    Returns all the amenity object
    """
    all_amenities = storage.all(Amenity)
    all_amenity_lists = []
    for amenity in all_amenities.values():
       all_amenity_lists.append(amenity.to_dict()) 
    return jsonify(all_amenity_lists)

@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def amenity_id(amenity_id):
    """
    Returns the Amenity with id amenity_id
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity = amenity.to_dict()
    return jsonify(amenity)

@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_id(amenity_id):
    """
    Delete the Amenity with id amenity_id
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route("/amenities/",
                 methods=["POST"],
                 strict_slashes=False)
def post_amenities():
    """
    Create a new amenity
    """
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return jsonify({"message": "Not a JSON"}), 400
    content = request.get_json()
    if "name" not in content:
        return jsonify({"message": "Missing name"}), 400
    amenity = Amenity()
    for key, value in content.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201

@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def put_amenity_id(amenity_id):
    """
    Put the Amenity with id amenity_id
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return jsonify({"message": "Not a JSON"}), 400
    content = request.get_json()
    for key, value in content.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
