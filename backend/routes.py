from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    
    picture = next((p for p in data if p.get("id") == id), None)

    if picture is not None:
        return jsonify(picture), 200
    return jsonify({"message": "picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture."""
    if not request.is_json:
        return jsonify({"Message": "Request body must be JSON"}), 400

    picture = request.get_json()

    for p in data:
        if p.get("id") == picture.get("id"):
            return (
                jsonify(
                    {
                        "Message": f"picture with id {picture['id']} already present"
                    }
                ),
                302,
            )

    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # get data from the json body
    picture_in = request.json
    for index, picture in enumerate(data):
        if picture["id"] == id:
            data[index] = picture_in
            return picture, 201
    return {"message": "picture not found"}, 404



######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by id."""
    # Search for the picture by id
    for picture in data:
        if picture.get("id") == id:
            data.remove(picture)
            # Return empty body with 204
            return "", 204

    # If not found, return 404
    return jsonify({"message": "picture not found"}), 404

