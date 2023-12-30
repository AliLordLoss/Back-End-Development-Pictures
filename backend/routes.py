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
    return data

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for pic in data:
        if pic["id"] == id:
            return pic
    return {"message": "picture not found!"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    pic = request.json
    if not pic:
        return {"message": "no picture provided!"}, 400
    if pic["id"] in [x["id"] for x in data]:
        return {"Message": f"picture with id {pic['id']} already present"}, 302
    data.append(pic)
    return pic, 201



######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pic = request.json
    if not pic:
        return {"message": "no picture provided!"}, 400
    for i in range(len(data)):
        if data[i]["id"] == pic["id"]:
            data[i] = pic
            return pic
    return {"Message": f"picture with id {pic['id']} not found!"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for i in range(len(data)):
        if data[i]["id"] == id:
            data.pop(i)
            return "", 204
    return {"message": "picture not found"}, 404
