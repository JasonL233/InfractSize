from app import db

class UploadedImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=True)

def to_json(self):
    return {
        "id": self.id,
        "filename": self.filename,
        "image": self.image
    }