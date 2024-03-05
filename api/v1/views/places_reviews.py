"""
Handles all the default RESTFul API actions for
places reviews
"""


from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from flask import abort, jsonify, request
from models import storage

@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False)
def place_reviews_id(place_id):
    """
    Returns the list of review of Place with id place_id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = place.reviews
    all_reviews = []
    for review in reviews:
        all_reviews.append(review.to_dict())
    return jsonify(all_reviews)

@app_views.route("/reviews/<review_id>", strict_slashes=False)
def review_id(review_id):
    """
    Returns the Review with id review_id
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review = review.to_dict()
    return jsonify(review)

@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review_id(review_id):
    """
    Delete the Review with id review_id
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200

@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """
    Create a new review for a Place
    """
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return jsonify({"message": "Not a JSON"}), 400
    content = request.get_json()
    if "text" not in content:
        return jsonify({"message": "Missing text"}), 400
    if "user_id" not in content:
        return jsonify({"message": "Missing user_id"}), 400
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    user_id = content["user_id"]
    user = storage.get(User, user_id)
    if not user_id:
        abort(404)
    review = Review()
    for key, value in content.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(review, key, value)
    review.place_id = place.id
    review.user_id = user.id
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201

@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def put_review_id(review_id):
    """
    Put the Place with id place_id
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return jsonify({"message": "Not a JSON"}), 400
    content = request.get_json()
    for key, value in content.items():
        if key not in ["id", "created_at", "updated_at", "place_id", "user_id"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
