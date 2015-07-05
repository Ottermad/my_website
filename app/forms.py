from flask_wtf import (
    Form,
)

from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
)

from wtforms.validators import (
    DataRequired,
    Email,
)


class LoginForm(Form):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class ProjectForm(Form):
    title = StringField("Title", validators=[DataRequired()])
    link = StringField("URL", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])


class PostForm(Form):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])


class ContactForm(Form):
    name = StringField("Name",validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    body = TextAreaField("Body", validators=[DataRequired()])
