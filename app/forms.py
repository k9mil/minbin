from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PasteForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired(), Length(max = 8192)])
    submit = SubmitField('Paste')