#!/usr/bin/python3
"""
Handles all the default RESTFul API actions for
places amenities
"""


from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from flask import abort, jsonify, request
from models import storage


@app_views.route("/places/<place_id>/amenities",
                 strict_slashes=False)
def place_amenities_id_place_id(place_id):
    """
    Returns the list of amenity of Place with id place_id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = place.amenities
    all_amenities = []
    for amenity in amenities:
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route("places/place_id/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_id_place_id(place_id, amenity_id):
    """
    Delete Amenity with amenity_id to Place of Place_id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity.place_id != place.id:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/amenity_id", methods=["POST"],
                 strict_slashes=False)
def post_amenity_place(place_id, amenity_id):
    """
    Create a new amenity for a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity.place_id != place_id:
        return jsonify(amenity.to_dict()), 200
    amenity.place_id = place_id
    return jsonify(amenity.to_dict()), 201
