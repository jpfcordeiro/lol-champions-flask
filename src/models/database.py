from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Champion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    lane = db.Column(db.String(150), nullable=False)

    # Método construtor
    def __init__(self, nome, lane):
        self.nome = nome
        self.lane = lane
