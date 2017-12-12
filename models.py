from app import db

class Posts(db.Model):
    __tablename__ = 'posts'
    id        = db.Column(db.Integer, primary_key = True)
    name      = db.Column(db.String)
    subject   = db.Column(db.String)
    date      = db.Column(db.String)
    text      = db.Column(db.Text)
