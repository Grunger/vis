from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()


#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
#app.config['SECRET_KEY'] = 'hlfwiuf76szd67stvgw.,m,m^^&%'
#db = SQLAlchemy(app)


class Users(db.Model):
    """Модель пользователя"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    surname = db.Column(db.String(20), unique=True)
    login = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(20), unique=False)
    password = db.Column(db.String(100), unique=False)

    def __repr__(self):
        return f'User: {self.login}, {self.email}'


class News(db.Model):
    """Таблица с новостями"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), unique=False)
    text = db.Column(db.String(1000), unique=False)
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'{self.title}: {self.text}'


class Best(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SingerName = db.Column(db.String(20), unique=False)
    achivment = db.Column(db.String(1024), unique=False)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Singers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SingerName = db.Column(db.String(20), unique=False)
    Geners_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    achivment = db.Column(db.String(1024), unique=False)
    Best = db.Column(db.Integer, db.ForeignKey('best.id'))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Genres(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo = db.Column(db.String(40), unique=False)
    title = db.Column(db.String(20), unique=False)
    text = db.Column(db.String(1000), unique=False)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))



class Music1(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    singers = db.Column(db.Integer, db.ForeignKey('singers.id'))
    Best = db.Column(db.Integer, db.ForeignKey('best.id'))
    date = db.Column(db.Date)
    genres = db.Column(db.Integer, db.ForeignKey('genres.id'))
    song = db.Column(db.String(40), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), unique=False)
    text = db.Column(db.String(1000), unique=False)
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


#db.create_all()
