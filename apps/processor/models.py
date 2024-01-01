from datetime import datetime

from apps.app import db

class Answer(db.Model):
    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String)
    image_path = db.Column(db.String)
    audio_path = db.Column(db.String)
    processed = db.Column(db.Boolean)
    threshold = db.Column(db.Integer)
    window_length = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)