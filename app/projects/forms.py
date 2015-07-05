from flask_wtf import (
    Form,
)

from wtforms import (
    StringField,
    TextAreaField,
)

from wtforms.validators import (
    DataRequired,
)

class ProjectForm(Form):
    title = StringField("Title", validators=[DataRequired()])
    link = StringField("URL", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])