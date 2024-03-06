#!/usr/bin/python3
"""
Manage the status and the stats of the app
"""

from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.user import User
from flask import jsonify
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.review import Review
from models.place import Place

models = [Amenity, City, Place, Review, State, User]

@app_views.route("/status", strict_slashes=False)
def status():
    """
    Returns the status of the app
    """
    return jsonify({"status": "OK"})

@app_views.route("/stats", strict_slashes=False)
def stats():
    """
    returns the stats of the app
    """
    return jsonify({
        "amenities": storage.count(Amenity), 
        "cities": storage.count(City), 
        "places": storage.count(Place), 
        "reviews": storage.count(Review), 
        "states": storage.count(State), 
        "users": storage.count(User)
        })
