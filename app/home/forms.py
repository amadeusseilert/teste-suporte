from wtforms import BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm


class NewPostForm(FlaskForm):
    text = TextAreaField('Text', validators=[DataRequired(), Length(min=1, max=256)])
    truth = BooleanField('Truth')

    submit = SubmitField('Post')

    def __init__(self, *args, **kwargs):
        super(NewPostForm, self).__init__(*args, **kwargs)
