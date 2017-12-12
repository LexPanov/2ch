from app import db

class Post(db.Model):
    __tablename__ = 'posts'
    id        = db.Column(db.Integer, primary_key = True)
    date      = db.Column(db.String)
    author    = db.Column(db.String)
    subject   = db.Column(db.String)
    body      = db.Column(db.String)