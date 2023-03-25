#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Article

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/get', methods=['GET', 'POST'])
def Article():
    if request.method == 'GET':
        articles = Article.query.all()
        articles_dict = [article.to_dict() for article in articles]
        return make_response(jsonify(articles_dict), 200)
    
    elif request.method == 'POST':
        data = request.get_json()
        new_article = Article(
            title = data.get('title'),
            body = data.get('body')
        )
        db.session.add(new_article)
        db.session.commit()

        return make_response(jsonify(new_article.to_dict()), 201)
        



@app.route('/get/<int:id>', methods= ['GET', 'DELETE', 'PATCH', 'PUT'])
def article_by_id(id):
    article = Article.query.filter(Article.id == id).first()

    if not article:
        return make_response(jsonify({'error': 'Article not found'}))

    if request.method == 'GET':
        return make_response(jsonify(article.to_dict()))
    
    elif request.method == 'DELETE':
        db.session.delete(article)
        db.session.commit()
        return make_response(jsonify({'success': 'delete success'}))
    
    elif request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(article, attr, data[attr])
        db.session.add(article)
        db.session.commit()
        return make_response(jsonify(article.to_dict()), 200)
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        title = data.get('title'),
        body = data.get('body')

        article.title = title
        article.body = body
        
        db.session.add(article)
        db.session.commit()

        return make_response(jsonify(article.to_dict()), 201)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
