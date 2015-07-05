from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    g,
    Markup,
    flash,
    jsonify,
)
from flask.ext.bcrypt import (
    check_password_hash,
)
from flask.ext.login import (
    current_user,
    LoginManager,
    login_required,
    logout_user,
    login_user,
)

from peewee import DoesNotExist

import forms
import models
import requests
import sendgrid
import markdown

key = open("key.txt")

app = Flask(__name__)
app.secret_key = key.readline().strip("\n")

sendgrid_creds = key.readline().strip("\n").split()
sendgrid_username = sendgrid_creds[0]
sendgrid_password = sendgrid_creds[1]
print(sendgrid_creds, sendgrid_username, sendgrid_password)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Functions
def remove_space(string):
    return string.replace(" ","-")


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to database before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each response"""
    g.db.close()
    return response

@app.route("/login/", methods=("GET", "POST"))
@app.route("/login", methods=("GET", "POST"))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except DoesNotExist:
            flash("Your email or password does not exist.", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in.", "success")
                return redirect(url_for("posts_blueprint.index"))
            else:
                flash("Your email or password does not exist.", "error")
    return render_template("login.html", form=form)


@app.route("/logout/")
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out. Come back soon.")
    return redirect(url_for("posts_blueprint.index"))


@app.route("/about/")
@app.route("/about")
def about():
    """Route for about page"""
    return render_template("about.html")


@app.route("/contact/", methods=["POST", "GET"])
@app.route("/contact", methods=["POST", "GET"])
def contact():
    form = forms.ContactForm()
    if form.validate_on_submit():
        sendgrid_object = sendgrid.SendGridClient(
            sendgrid_username, sendgrid_password)
        message = sendgrid.Mail()
        sender = form.email.data
        subject = form.name.data
        body = form.body.data
        message.add_to("charlie.thomas@attwoodthomas.net")
        message.set_from(sender)
        message.set_subject(subject)
        message.set_html(body)
        r = sendgrid_object.send(message)
        print(r)
        flash("Email sent.")
        return redirect(url_for("contact"))
    else:
        return render_template("contact.html", form=form)


@app.route("/science")
def science():
    return render_template("science.html")


from app.posts.views import posts_blueprint
app.register_blueprint(posts_blueprint)

from app.projects.views import projects_blueprint
app.register_blueprint(projects_blueprint)

from app.treehouse.views import treehouse_blueprint
app.register_blueprint(treehouse_blueprint)

app.jinja_env.filters['remove_space'] = remove_space



"""
if __name__ == "__main__":
    app.jinja_env.filters['remove_space'] = remove_space
    app.run(debug=True)
"""