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

import forms
import models
import requests
import sendgrid
import markdown

COLORS = {
    "Ruby": "#F7464A",
    "Android": "#51B46D",
    "JavaScript": "#C25975",
    "Python": "#F092B0",
    "HTML": "#39ADD1",
    "CSS": "#3079AB",
    "PHP": "#7D669E",
    "Development Tools": "#637A91",
    "Business": "#F9845B",
    "iOS": "#53BBB4",
    "Design": "#E0AB18",
    "Java": "#2C9676",
    "WordPress": "#838CC7",
    "Digital Literacy": "#C38CD4",
}
NUMBER_OF_COURSES = 12
TREEHOUSE_USER = "charliethomas"

key = open("key.txt")

app = Flask(__name__)
app.secret_key = key.readline().strip("\n")

sendgrid_creds = key.readline().strip("\n")
sendgrid_username = sendgrid_creds[0]
sendgrid_password = sendgrid_creds[1]
print(sendgrid_username, sendgrid_password)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Functions
def remove_space(string):
    return string.replace(" ","-")

def get_points():
    try:
        my_request = requests.get(
            "http://teamtreehouse.com/{}.json".format(TREEHOUSE_USER)
        )
        try:
            if my_request.status_code == 200:
                json = my_request.json()  # Get JSON
                subject_points = json["points"]  # Get points
                return subject_points
            else:
                print("Status Code Error: {}".format(my_request.status_code))
        except:
            # Error parsing json
            print("Invalid JSON.")
    except:
        # Error with url
        print("Request error.")


def get_number_of_subjects():
    try:
        my_request = requests.get(
            "http://teamtreehouse.com/{}.json".format(TREEHOUSE_USER)
        )
        try:
            if my_request.status_code == 200:
                json = my_request.json()  # Get JSON
                subject_points = json["points"]  # Get points
                return len(subject_points)
            else:
                print("Status Code Error: {}".format(my_request.status_code))
        except:
            # Error parsing json
            print("Invalid JSON.")
    except:
        # Error with url
        print("Request error.")


def get_courses(number_of_courses):
    try:
        my_request = requests.get(
            "http://teamtreehouse.com/{}.json".format(TREEHOUSE_USER)
        )
        try:
            if my_request.status_code == 200:
                json = my_request.json()  # Get JSON
                badges = json["badges"]  # Get points
                badges = badges[-number_of_courses:]
                badges.reverse()
                return badges
            else:
                print("Status Code Error: {}".format(my_request.status_code))
        except:
            # Error parsing json
            print("Invalid JSON.")
    except:
        # Error with url
        print("Request error.")


def order_points(points):
    return sorted(points.items(), key=lambda x: x[1])[::-1]


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
        except models.DoesNotExist:
            flash("Your email or password does not exist.", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in.", "success")
                return redirect(url_for("index"))
            else:
                flash("Your email or password does not exist.", "error")
    return render_template("login.html", form=form)

@app.route("/logout/")
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out. Come back soon.")
    return redirect(url_for("index"))






@app.route("/about/")
@app.route("/about")
def about():
    """Route for about page"""
    return render_template("about.html")





@app.route("/points/")
@app.route("/points")
def points():
    """points = order_points(get_points())
    courses = get_courses(NUMBER_OF_COURSES)
    context = {
        "points": points,
        "courses": courses,
        "colors": COLORS,
        "username": TREEHOUSE_USER,
    }"""
    return render_template("points.html", username=TREEHOUSE_USER)


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
        sendgrid_object.send(message)
        flash("Email sent.")
        return redirect(url_for("contact"))
    else:
        return render_template("contact.html", form=form)



@

@app.route("/post_json/", methods=["POST", "GET"])
@app.route("/post_json", methods=["POST", "GET"])
def post_json():
    posts = models.Post.get_posts()[::-1]
    return jsonify(results=posts)

@app.route("/science")
def science():
    return render_template("science.html")

if __name__ == "__main__":
    app.jinja_env.filters['remove_space'] = remove_space
    app.run(debug=True)
