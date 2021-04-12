import os
import sqlite3

from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import Session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, AddNews, AddSingers, AddGenres, AddBest, SearchForm, FilterForm, AddMusic, \
    AddComments
from models import Users
from userlogin import UserLogin
from models import News
from models import Singers, Genres, Best, Music1, Comments
from werkzeug.utils import secure_filename
import datetime as dt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'hlfwiuf76szd67stvgw.,m,m^^&%'
db = SQLAlchemy(app)
engine = create_engine('sqlite:///db.sqlite', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
# db.create_all()
login_manager = LoginManager(app)

"""" Фнкции,основной код """


# photos = UploadSet('photos', IMAGES)
# configure_uploads(app, photos)
# patch_request_class(app)  # set maximum file size, default is 16MB

# pages
@app.route('/')
def index():
    return render_template('index.html', title='Main page')


@login_manager.user_loader
def load_user(user_id):
    # print("load_user")
    return UserLogin().fromDB(user_id, Users)


"""-НОВОСТИ-"""


@app.route('/news', methods=['POST', 'GET'])
@login_required
def news():
    if request.method == 'GET':
        db_sess = Session()
        news = db_sess.query(News).order_by(News.date).all()[::-1]
        db_sess.close()
    form_search = SearchForm()
    form_filter = FilterForm(author=[1, 2, 3])
    db_sess = Session()
    users = db_sess.query(Users).all()
    form_filter.author.choices = [(user.id, user.login) for user in users]
    author1 = (' '.join([(user.login) for user in users]))
    if form_search.submit1.data:
        text = form_search.title.data
        db_sess = Session()
        news = db_sess.query(News).filter(or_(News.title.like(f'%{text}%'), News.text.like(f'%{text}%'))).all()
        db_sess.close()
    if form_filter.submit2.data:
        if form_filter.date_from.data:
            date_from = form_filter.date_from.data
        else:
            date_from = dt.date(1900, 1, 1)
        if form_filter.date_to.data:
            date_to = form_filter.date_to.data
        else:
            date_to = dt.date.today()
        ids = form_filter.author.data
        db_sess = Session()
        if not ids:
            ids = [i[0] for i in db_sess.query(Users.id).all()]
        news = db_sess.query(News).filter(News.date.between(date_from, date_to)).filter(News.user_id.in_(ids)).all()
        db_sess.close()
    for item in news:
        item.text = item.text.split('|')

    return render_template('news.html', title='Новости', news=news, form_search=form_search, form_filter=form_filter,
                           author1=author1)


@app.route('/news/<int:n>', methods=['GET', 'DELETE'])
def news_one(n):
    if request.method == 'GET':
        db_sess = Session()
        news = db_sess.query(News).filter(News.id == n).first()
        news.text = news.text.split('|')
        db_sess.close()
        return render_template('news_one.html', title='News', news=news)
    elif request.method == 'DELETE':
        db_sess = Session()
        db_sess.query(News).delete(News.id == n)
        db_sess.close()
        return redirect('/news')


@app.route('/change_news/<int:n>', methods=['POST', 'GET'])
def change_news(n):
    form = AddNews()
    if request.method == "GET":
        db_sess = Session()
        news = db_sess.query(News).filter(News.id == n).first()
        db_sess.close()
        form.title.data = news.title
        form.text.data = news.text
        form.date.data = news.date

    if form.validate_on_submit():
        news = News()
        news.id = n
        news.title = form.title.data
        text = form.text.data
        news.text = text.replace('\n', '|')
        news.date = form.date.data
        news.user_id = current_user.get_id()
        db.session.merge(news)
        db.session.commit()
        flash('News has been added')
        return redirect('/news')

    return render_template('add_news.html', form=form)


@app.route('/delete_news/<int:n>', methods=['POST', 'GET'])
def delete_news(n):
    db_sess = Session()
    news = db_sess.query(News).filter(News.id == n).first()
    if not news:
        abort(404)
    if str(news.user_id) != current_user.get_id():
        abort(400)
    db_sess.delete(news)
    db_sess.commit()
    return redirect('/news')


@app.route('/add_news', methods=['POST', 'GET'])
def add_news():
    form = AddNews()
    form.date.data = dt.date.today()
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        text = text.replace('\n', '|')
        date = form.date.data
        id = current_user.get_id()
        news = News(title=title,
                    text=text,
                    date=date,
                    user_id=id)
        db.session.add(news)
        db.session.commit()
        flash('News has been added')

    return render_template('add_news.html', form=form)


"""Авторизация"""

"""-Певцы-"""


@app.route('/singers', methods=['POST', 'GET'])
def singers():
    if request.method == 'GET':
        db_sess = Session()
        singers = db_sess.query(Singers).order_by(Singers.date).all()[::-1]
        db_sess.close()

    return render_template('singers.html', title='singers', singers=singers)


@app.route('/delete_singers/<int:n>', methods=['POST', 'GET'])
def delete_singers(n):
    db_sess = Session()
    singers = db_sess.query(Singers).filter(Singers.id == n).first()
    if not singers:
        abort(404)
    """if str(Singers.user_id) != current_user.get_id():
        abort(400)"""
    db_sess.delete(singers)
    db_sess.commit()
    return redirect('/singers')


@app.route('/change_singers/<int:n>', methods=['POST', 'GET'])
def change_singers(n):
    form = AddSingers()
    form.date.data = dt.date.today()
    if request.method == "GET":
        db_sess = Session()
        singers = db_sess.query(Singers).filter(Singers.id == n).first()
        db_sess.close()
        form.SingerName.data = singers.SingerName
        form.achivment.data = singers.achivment
        form.date.data = singers.date

    if form.validate_on_submit():
        singers = Singers()
        singers.id = n
        singers.SingerName = form.SingerName.data
        achivment = form.achivment.data
        singers.achivment = achivment.replace('\n', '|')
        singers.date = form.date.data
        singers.user_id = current_user.get_id()
        db.session.merge(singers)
        db.session.commit()
        flash('News has been added')
        return redirect('/singers')

    return render_template('add_singers.html', form=form)


@app.route('/add_singers', methods=['POST', 'GET'])
def add_singers():
    form = AddSingers()
    form.date.data = dt.date.today()
    if form.validate_on_submit():
        SingerName = form.SingerName.data
        achivment = form.achivment.data
        date = form.date.data
        id = current_user.get_id()
        singers = Singers(
            SingerName=SingerName,
            achivment=achivment,
            date=date,
            user_id=id)
        db.session.add(singers)
        db.session.commit()
        flash('Singers has been added')

    return render_template('add_singers.html', form=form)


"""-ЖАНРЫ-"""


@app.route('/genres')
def genres():
    db_sess = Session()
    genres = db_sess.query(Genres).order_by(Genres.date).all()[::-1]
    db_sess.close()
    for item in genres:
        item.text = item.text.split('|')
    return render_template('genres.html', title='genres', genres=genres)


@app.route('/add_genres', methods=['POST', 'GET'])
def add_genres():
    form = AddGenres()
    form.date.data = dt.date.today()
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        text = text.replace('\n', '|')
        id = current_user.get_id()
        date = form.date.data
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(os.path.join('static', 'images', filename))
        genres = Genres(
            photo=filename,
            date=date,
            title=title,
            text=text,
            user_id=id)
        db.session.add(genres)
        db.session.commit()
        flash('Genres has been added')
    return render_template('add_genres.html', form=form)


@app.route('/genres/<int:n>', methods=['GET', 'DELETE'])
def genres_one(n):
    db_sess = Session()
    music = db_sess.query(Music1).order_by(Music1.date).all()[::-1]
    db_sess.close()
    if request.method == 'GET':
        db_sess = Session()
        genres = db_sess.query(Genres).filter(Genres.id == n).first()
        genres.text = genres.text.split('|')
        db_sess.close()
        return render_template('genres_one.html', title='News', genres=genres, music=music)


@app.route('/add_music', methods=['POST', 'GET'])
def add_music():
    form = AddMusic()
    if form.validate_on_submit():
        f = form.song.data
        filename = secure_filename(f.filename)
        f.save(os.path.join('static', 'mp3', filename))
        id = current_user.get_id()
        music = Music1(
            song=filename,
            user_id=id
        )
        db.session.add(music)
        db.session.commit()
        flash('Music has been added')

    return render_template('add_music.html', form=form)


@app.route('/delete_music/<int:n>', methods=['POST', 'GET'])
def delete_music(n):
    db_sess = Session()
    music = db_sess.query(Music1).filter(Music1.id == n).first()

    db_sess.delete(music)
    db_sess.commit()
    return redirect('genres_one.html')


@app.route('/change_genres/<int:n>', methods=['POST', 'GET'])
def change_genres(n):
    form = AddGenres()
    form.date.data = dt.date.today()
    if request.method == "GET":
        db_sess = Session()
        genres = db_sess.query(Genres).filter(Genres.id == n).first()
        db_sess.close()
        form.title.data = genres.title
        form.text.data = genres.text
        form.date.data = genres.date

    if form.validate_on_submit():
        genres = Genres()
        genres.id = n
        genres.title = form.title.data
        text = form.text.data
        genres.text = text.replace('\n', '|')
        genres.date = form.date.data
        genres.user_id = current_user.get_id()
        db.session.merge(genres)
        db.session.commit()
        flash('News has been added')
        return redirect('/genres')

    return render_template('add_genres.html', form=form)


@app.route('/delete_genres/<int:n>', methods=['POST', 'GET'])
def delete_genres(n):
    db_sess = Session()
    genres = db_sess.query(Genres).filter(Genres.id == n).first()
    if not genres:
        abort(404)
    if str(genres.user_id) != current_user.get_id():
        abort(400)
    db_sess.delete(genres)
    db_sess.commit()
    return redirect('/genres')


"""---"""


@app.route('/best', methods=['POST', 'GET'])
def best():
    if request.method == 'GET':
        db_sess = Session()
        best = db_sess.query(Best).order_by(Best.date).all()[::-1]
        db_sess.close()

    return render_template('best.html', title='singers', best=best)


@app.route('/add_best', methods=['POST', 'GET'])
def add_best():
    form = AddBest()
    form.date.data = dt.date.today()
    if form.validate_on_submit():
        SingerName = form.SingerName.data
        achivment = form.achivment.data
        date = form.date.data
        id = current_user.get_id()
        best = Best(
            SingerName=SingerName,
            achivment=achivment,
            date=date,
            user_id=id)
        db.session.add(best)
        db.session.commit()
        flash('Singers has been added')

    return render_template('add_best.html', form=form)


@app.route('/information')
def information():
    return render_template('base.html', title='Information')


""" -Комменты- """


@app.route('/comments', methods=['POST', 'GET'])
def comments():
    if request.method == 'GET':
        db_sess = Session()
        comments = db_sess.query(Comments).order_by(Comments.date).all()[::-1]
        # users1 = current_user.get(login)
        # users = db_sess.query(Users).all()
        # author1 = (' '.join([(user.login) for user in users1]))

        db_sess.close()
    for item in comments:
        item.text = item.text.split('|')
    return render_template('comments.html', title='Comments', comments=comments, )


@app.route('/add_comments', methods=['POST', 'GET'])
def add_comments():
    form = AddComments()
    form.date.data = dt.date.today()
    if form.validate_on_submit():
        db_sess = Session()
        user = db_sess.query(Users)
        db_sess.close()
        # log = user.get(login)
        title = form.title.data
        text = form.text.data
        text = text.replace('\n', '|')
        date = form.date.data
        id = current_user.get_id()
        comments = Comments(title=title,
                            text=text,
                            date=date,
                            user_id=id
                            )
        db.session.add(comments)
        db.session.commit()
        flash('Comment has been added')

    return render_template('add_comments.html', form=form)


@app.route('/delete_comments/<int:n>', methods=['POST', 'GET'])
def delete_comments(n):
    db_sess = Session()
    comments = db_sess.query(Comments).filter(Comments.id == n).first()
    if not comments:
        abort(404)
    if str(comments.user_id) != current_user.get_id():
        abort(400)
    db_sess.delete(comments)
    db_sess.commit()
    return redirect('/comments')


@app.route('/change_comment/<int:n>', methods=['POST', 'GET'])
def change_comment(n):
    form = AddComments()
    form.date.data = dt.date.today()
    if request.method == "GET":
        db_sess = Session()
        comments = db_sess.query(Comments).filter(Comments.id == n).first()
        db_sess.close()
        form.title.data = comments.title
        form.text.data = comments.text
        form.date.data = comments.date

    if form.validate_on_submit():
        comments = Comments()
        comments.id = n
        comments.title = form.title.data
        text = form.text.data
        comments.text = text.replace('\n', '|')
        comments.date = form.date.data
        comments.user_id = current_user.get_id()
        db.session.merge(comments)
        db.session.commit()
        flash('Comment has been added')
        return redirect('/comments')

    return render_template('add_comments.html', form=form)


"""-ВХОД-"""


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        user = Users.query.filter_by(login=login).first()
        if user is None:
            flash('Такой пользователь не существует')
            return render_template('login.html', title='Авторизация', form=form)
        if not check_password_hash(user.password, password):
            flash('Неверный пароль')
            return render_template('login.html', title='Авторизация', form=form)
        user_login = UserLogin().create(user)
        login_user(user_login)
        flash('Вы успешно вошли')
    return render_template('login.html', title='Авторизация', form=form)


"""-ВЫХОД-"""


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


"""-РЕГИСТРАЦИЯ-"""


@app.route('/register', methods=['POST', 'GET'])
def register():
    try:
        form = RegisterForm()
        if form.validate_on_submit():
            name = form.name.data
            surname = form.surname.data
            login = form.login.data
            email = form.email.data
            password = generate_password_hash(form.password.data)
            user = Users(login=login,
                         name=name,
                         surname=surname,
                         email=email,
                         password=password)
            db.session.add(user)
            db.session.commit()
            flash('Успешная регистрация')
            return redirect(url_for('index'))
    except sqlite3.IntegrityError:
        print("Oops!  That was no valid number.  Try again...")

    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(debug=True)
