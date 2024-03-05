"""
Handles all the default RESTFul API actions for the app
"""


from api.v1.views import app_views
from models.state import State
from flask import abort, jsonify, request
from models import storage

@app_views.route("/states/", strict_slashes=False)
def states():
    """
    Returns all the state object
    """
    all_states = storage.all(State)
    all_state_lists = []
    for state in all_states.values():
       all_state_lists.append(state.to_dict()) 
    return jsonify(all_state_lists)

@app_views.route("/states/<state_id>", strict_slashes=False)
def state_id(state_id):
    """
    Returns the State with id state_id
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state = state.to_dict()
    return jsonify(state)

@app_views.route("/states/<state_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_state_id(state_id):
    """
    Delete the State with id state_id
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route("/states/",
                 methods=["POST"],
                 strict_slashes=False)
def post_state():
    """
    Create a new state
    """
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return jsonify({"message": "Not a JSON"}), 400
    content = request.get_json()
    if "name" not in content:
        return jsonify({"message": "Missing name"}), 400
    state = State()
    for key, value in content.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

@app_views.route("/states/<state_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def put_state_id(state_id):
    """
    Put the State with id state_id
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return jsonify({"message": "Not a JSON"}), 400
    content = request.get_json()
    for key, value in content.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
