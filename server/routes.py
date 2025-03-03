import os
import shutil
from app import app, db
from flask import request, jsonify
from models import Friend

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

file_counts = {
    "images": 0,
    "targetMasks": 0,
    "totalMasks": 0
}

# Function to clear all folders before upload
def clear_upload_folder():
    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)  # Remove the entire folder
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Recreate root upload folder
    os.makedirs(os.path.join(UPLOAD_FOLDER, "images"), exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_FOLDER, "targetMasks"), exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_FOLDER, "totalMasks"), exist_ok=True)


# Upload images
@app.route("/api/upload", methods=["POST"]) 
def upload_images():
    clear_upload_folder()

    if "files" not in request.files:
        return jsonify({"error": "No files uploaded"}), 400
    
    files = request.files.getlist("files")
    folders = request.form.getlist("folders")

    if len(files) != len(folders):
        return jsonify({"error": "Mismatch between files and folders"}), 400

    uploaded_files = []
    for file, folder in zip(files, folders):
        file_counts[folder] += 1
        index = file_counts[folder]

        if (folder == "images"):
            new_filename = f"{index}.png"
        elif (folder == "targetMasks"):
            new_filename = f"targetMask{index}.png"
        else:
            new_filename = f"totalMask{index}.png"
        
        folder_path = os.path.join(app.config["UPLOAD_FOLDER"], folder)
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, new_filename)
        file.save(file_path)
        
        uploaded_files.append(file_path)



    return jsonify({"message": "Files uploaded successfully!", "files": uploaded_files}), 200
        
