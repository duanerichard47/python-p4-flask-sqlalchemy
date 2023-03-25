from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())
    created_at = db.Column(db.DateTime,server_default=db.func.now() )
    updated_at = db.Column(db.DateTime,onupdate=db.func.now())

    def __init__(self, title, body):
        self.title = title
        self.body = body
