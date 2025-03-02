from app import app, db
from flask import request, jsonify
from models import UploadedImages

# Fetch images
@app.route("/api/images", methods=["GET"]) 
def get_images():
    images = UploadedImages.query.all()
    result = [image.to_json() for image in images]
    return jsonify(result)  # Status 200 in default
