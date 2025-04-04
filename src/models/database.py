from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Champion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    lane = db.Column(db.String(150), nullable=False)

    def __init__(self, nome, lane):
        self.nome = nome
        self.lane = lane

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    upload_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, filename, title, description):
        self.filename = filename
        self.title = title
        self.description = description
