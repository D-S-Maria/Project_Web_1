from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class AddJourney(FlaskForm):
    country = StringField('Country', validators=[DataRequired()])
    user_id = IntegerField('User id', validators=[DataRequired()])
    about = StringField('About', validators=[DataRequired()])
    month = StringField('Month', validators=[DataRequired()])
    transport = StringField('Transport', validators=[DataRequired()])

    submit = SubmitField('Submit')
