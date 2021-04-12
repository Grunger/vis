from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectMultipleField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields.html5 import DateField


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('SurName', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=4)])
    login = StringField('Логин', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddNews(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Content', validators=[DataRequired()])
    date = DateField('Enter date')
    submit = SubmitField('Add')


class AddComments(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Content', validators=[DataRequired()])
    date = DateField('Enter date')
    submit = SubmitField('Add')


class AddGenres(FlaskForm):
    photo = FileField('Title', validators=[FileRequired()])
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Content', validators=[DataRequired()])
    date = DateField('Enter date')
    submit = SubmitField('Add')


class AddSingers(FlaskForm):
    SingerName = StringField('Name', validators=[DataRequired()])
    achivment = TextAreaField('Content', validators=[DataRequired()])
    date = DateField('Enter date')
    submit = SubmitField('Add')


class AddBest(FlaskForm):
    SingerName = StringField('Name', validators=[DataRequired()])
    achivment = TextAreaField('Content', validators=[DataRequired()])
    date = DateField('Enter date')
    submit = SubmitField('Add')


# class Music2(FlaskForm):
#  song = FileField('Title', validators=[FileRequired()])

class AddMusic(FlaskForm):
    # song  = FieldList(FormField(Music2),  min_entries=2)
    song = FileField('Title', validators=[FileRequired()])
    submit = SubmitField('Add')


class SearchForm(FlaskForm):
    title = StringField('Поиск по тексту')
    submit1 = SubmitField('search')


class FilterForm(FlaskForm):
    date_from = DateField('дата от')
    date_to = DateField('до')
    author = SelectMultipleField('Autor')
    submit2 = SubmitField('search')
