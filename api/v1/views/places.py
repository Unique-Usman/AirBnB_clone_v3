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
from os import getenv

STORAGE_TYPE = getenv('HBNB_TYPE_STORAGE')



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

@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """
        places route to handle http method for request to search places
    """
    all_places = [p for p in storage.all('Place').values()]
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    states = req_json.get('states')
    if states and len(states) > 0:
        all_cities = storage.all('City')
        state_cities = set([city.id for city in all_cities.values()
                            if city.state_id in states])
    else:
        state_cities = set()
    cities = req_json.get('cities')
    if cities and len(cities) > 0:
        cities = set([
            c_id for c_id in cities if storage.get('City', c_id)])
        state_cities = state_cities.union(cities)
    amenities = req_json.get('amenities')
    if len(state_cities) > 0:
        all_places = [p for p in all_places if p.city_id in state_cities]
    elif amenities is None or len(amenities) == 0:
        result = [place.to_json() for place in all_places]
        return jsonify(result)
    places_amenities = []
    if amenities and len(amenities) > 0:
        amenities = set([
            a_id for a_id in amenities if storage.get('Amenity', a_id)])
        for p in all_places:
            p_amenities = None
            if STORAGE_TYPE == 'db' and p.amenities:
                p_amenities = [a.id for a in p.amenities]
            elif len(p.amenities) > 0:
                p_amenities = p.amenities
            if p_amenities and all([a in p_amenities for a in amenities]):
                places_amenities.append(p)
    else:
        places_amenities = all_places
    result = [place.to_json() for place in places_amenities]
    return jsonify(result)
