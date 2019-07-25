import flask_restless
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_pyfile('config.cfg')


db = SQLAlchemy(app)

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    TITLE = db.Column(db.String(600))
    SOURCE = db.Column(db.String(600),unique=True)
    DATE = db.Column(db.String(80))
    CONTENT = db.Column(db.String(12255))
    articlecategories = db.relationship('Articlecategorie', backref= 'article', lazy='dynamic')
    geotags = db.relationship('Geotag', backref= 'article', lazy='dynamic')

    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'))

class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domainname = db.Column(db.String(600), unique=True)
    desc = db.Column(db.String(80))
    articles = db.relationship('Article', backref= 'domain', lazy='dynamic')


class Articlecategorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.String(250))

    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'))

class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    desc = db.Column(db.String(250))
    articlecategories = db.relationship('Articlecategorie', backref= 'categorie', lazy='dynamic')
    topicmodels = db.relationship('Topicmodel', backref= 'categorie', lazy='dynamic')


class Geotag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    locdesc = db.Column(db.String(250))
    location = db.Column(db.String(250))

    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    
class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(355),unique=True)
    topicmodel = db.relationship('Topicmodel', backref= 'Keyword', lazy='dynamic')
    
    
class Topicmodel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    keyword_id = db.Column(db.Integer, db.ForeignKey('keyword.id'))
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'))

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
restless_manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

if __name__ == '__main__':
    manager.run()
