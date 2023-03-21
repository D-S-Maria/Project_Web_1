from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class AddJourney(FlaskForm):
    country = StringField('Страна', validators=[DataRequired()])
    about = StringField('План путешествия', validators=[DataRequired()])
    month = StringField('Планируемая дата', validators=[DataRequired()])
    transport = StringField('Транспорт', validators=[DataRequired()])

    submit = SubmitField('Предложить')
